"""Parallel review downloader"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from itertools import count, zip_longest
from functools import partial
from typing import Any, Callable, Optional, cast

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from typing_extensions import Self

from .exceptions import CAPTCHAError, AccountProtectionError
from .dicts import Reviews, Review


class AmazonScraper:
    """
    Amazon scraper to fetch reviews from products with multi-threading
    with support for logging in and captcha handling

    To set custom handlers for CAPTCHAs, modify the `captcha_handler` attribute
    """

    def __init__(self, fake_display: bool = True) -> None:
        opts = FirefoxOptions()
        if fake_display:
            opts.add_argument("--headless")  # type: ignore

        with ThreadPoolExecutor() as executor:
            self.browsers: list[Firefox] = list(
                map(
                    lambda fut: fut.result(),
                    as_completed(
                        [executor.submit(Firefox, options=opts) for _ in range(5)]
                    ),
                )
            )

        self.captcha_handler = self.handle_captcha

    def handle_captcha(self, future: Future, browsers: list) -> None:
        """Default CAPTCHA handler"""
        try:
            future.result()
        except AccountProtectionError as e:
            browser: Firefox = next(  # type: ignore
                b for b in self.browsers if b.session_id == e.browser_id
            )
            captcha = input(
                f"(login) Please solve the captcha for {self.browsers.index(browser)}: "
            )
            browser.find_element(
                By.CSS_SELECTOR, "input[name=cvf_captcha_input]"
            ).send_keys(captcha)
            browser.find_element(
                By.CSS_SELECTOR, "input[name=cvf_captcha_captcha_action]"
            ).click()
            browsers.append(browser)
        except CAPTCHAError as e:
            browser_: Firefox = next(
                b for b in self.browsers if b.session_id == e.browser_id
            )
            browser_.execute_script(  # type: ignore
                f"document.querySelector('p.a-last').innerHTML += '<b>(Browser {self.browsers.index(browser_)})</b>'"
            )
            captcha = input(
                f"(enter) Please solve the captcha for {self.browsers.index(browser_)}: "
            )
            browser_.find_element(By.ID, "captchacharacters").send_keys(captcha)
            browser_.find_element(By.CSS_SELECTOR, "button.a-button-text").click()
            browsers.append(browser_)

    def _login_single(self, browser: Firefox, email: str, password: str) -> None:
        browser.get("https://amazon.com")
        try:
            if (
                "Sorry, we just need to make sure you're not a robot"
                in browser.page_source
            ):
                raise CAPTCHAError(browser.session_id)
            browser.find_element(By.ID, "nav-link-accountList").click()
            browser.find_element(By.ID, "ap_email").send_keys(email)
            browser.find_element(By.ID, "continue").click()
            browser.find_element(By.ID, "ap_password").send_keys(password)
            browser.find_element(By.ID, "signInSubmit").click()
            if browser.title == "Authentication required":
                raise AccountProtectionError(browser.session_id)
        except NoSuchElementException:
            self._login_single(browser, email, password)

    def login(self, email: str, password: str) -> None:
        """Log in all browsers to Amazon with an email and password"""

        captchad_browsers: list[Firefox] = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._login_single, browser, email, password)
                for browser in self.browsers
            ]
            for f in as_completed(futures):
                f.add_done_callback(
                    partial(self.captcha_handler, browsers=captchad_browsers)
                )
        if captchad_browsers:
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self._login_single, browser, email, password)
                    for browser in captchad_browsers
                ]

    @staticmethod
    def select_reviews(content: Any) -> list[Review]:
        """Select reviews from a Amazon page source"""
        reviews = []
        for review in content:
            row = review.select_one(".a-row")
            if row is not None:
                try:
                    rating = int(
                        row.select_one("i[data-hook='review-star-rating']").text.split(
                            "."
                        )[0]
                    )
                except AttributeError:
                    rating = -1
                body = row.select_one("span[data-hook='review-body']").text
                reviews.append(
                    cast(Review, {"reviewText": body.strip(), "overall": rating})
                )
        return reviews

    def _scrape_single(
        self,
        browser: Firefox,
        asin: str,
        category: int,
        callback: Callable[[Reviews], Any],
        limit: Optional[int] = None,
    ) -> None:
        map_star = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

        if limit:
            counter = count(0)
        for page in range(1, 11):
            print("browser", category, "page", page)
            browser.get(
                f"https://www.amazon.com/product-reviews/{asin}/"
                f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page}&filterByStar={map_star[category]}_star"
            )
            soup = BeautifulSoup(browser.page_source, "html.parser")
            content = soup.select("div[data-hook='review']")
            items = []
            for item in self.select_reviews(content):
                if next(counter) >= limit:  # type: ignore
                    return
                items.append(item)
            callback({"items": items, "productId": asin})

    def scrape(
        self,
        asin: str,
        callback: Callable[[Reviews], Any],
        proportions: Optional[list[int]] = None,
    ) -> None:
        """Scrape reviews from all star categories on a product page given an ASIN.

        - `callback` is a function which consumes results
        - `proportions` is a list of the number of reviews to scrape from each category
        (none by default)

        Note that callback functions are not run as thread-safe. Use threadinglocks where appropriate
        """
        if not proportions:
            proportions = []

        futures = []
        with ThreadPoolExecutor() as executor:
            for i, browser, prop in zip_longest(
                range(1, 6), self.browsers, proportions
            ):
                futures.append(
                    executor.submit(
                        self._scrape_single, browser, asin, i, callback, prop
                    )
                )

    def close(self) -> None:
        """Close all browsers"""
        with ThreadPoolExecutor() as executor:
            for browser in self.browsers:
                executor.submit(browser.quit)

    # these methods are practically useless at this point
    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
