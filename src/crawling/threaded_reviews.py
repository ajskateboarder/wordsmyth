"""Parallel review downloader"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from itertools import count, zip_longest
from functools import partial
from typing import Any, Callable, Generator, Optional

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from typing_extensions import Self


class CAPTCHAError(Exception):
    def __init__(self, browserId: str | None) -> None:
        self.browserId = browserId


class AccountProtectionError(Exception):
    pass


class AmazonScraper:
    """
    Amazon scraper to fetch reviews from products with multi-threading
    with support for logging in and captcha handling

    To set a custom handler for CAPTCHAs, modify the `captcha_handler` attribute
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

        self.captcha_handler = self._handle_captcha

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
        except NoSuchElementException:
            self._login_single(browser, email, password)

    def _handle_captcha(self, future: Future, browsers: list) -> None:
        try:
            future.result()
        except CAPTCHAError as e:
            browser: Firefox = next(
                b for b in self.browsers if b.session_id == e.browserId
            )
            browser.execute_script(  # type: ignore
                f"document.querySelector('p.a-last').innerHTML += '<b>(Browser {self.browsers.index(browser)})</b>'"
            )
            captcha = input(
                f"Please solve the captcha for {self.browsers.index(browser)}: "
            )
            browser.find_element(By.ID, "captchacharacters").send_keys(captcha)
            browser.find_element(By.CSS_SELECTOR, "button.a-button-text").click()
            browsers.append(browser)

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
    def select_reviews(content: Any) -> Generator[dict, None, None]:
        """Select reviews from a Amazon page source"""
        for review in content:
            row = review.select_one(".a-row")
            if row is not None:
                rating = int(
                    row.select_one("i[data-hook='review-star-rating']").text.split(".")[
                        0
                    ]
                )
                body = row.select_one("span[data-hook='review-body']").text
                yield {"reviewText": body.strip(), "overall": rating}

    def _scrape_single(
        self,
        browser: Firefox,
        asin: str,
        category: int,
        callback: Callable[[dict], Any],
        limit: Optional[int] = None,
    ) -> None:
        map_star = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

        if limit:
            counter = count(0)
        for page in range(1, 11):
            browser.get(
                f"https://www.amazon.com/product-reviews/{asin}/"
                f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page}&filterByStar={map_star[category]}"
            )
            soup = BeautifulSoup(browser.page_source, "html.parser")
            content = soup.select("div[data-hook='review']")
            for item in self.select_reviews(content):
                if next(counter) >= limit:  # type: ignore
                    return
                callback({**item, "productId": asin})

    def scrape(
        self,
        asin: str,
        callback: Callable[[dict], Any],
        proportions: Optional[list[int]] = None,
    ) -> None:
        """Scrape reviews from all star categories on a product page given an ASIN

        - `callback` is a function which consumes results
        - `proportions` is a list of the number of reviews to scrape from each category
        (none by default)
        """
        if not proportions:
            proportions = []

        with ThreadPoolExecutor() as executor:
            for i, browser, prop in zip_longest(
                range(1, 6), self.browsers, proportions
            ):
                future = executor.submit(
                    self._scrape_single,
                    browser,
                    asin,
                    i,
                    callback,
                    prop,  # ctx
                )
                if future.exception():
                    raise future.exception()  # type: ignore

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
