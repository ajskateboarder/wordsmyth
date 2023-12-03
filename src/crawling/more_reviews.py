"""Parallel review downloader"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import count, repeat, zip_longest
from typing import Any, Callable, Generator, Optional

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from typing_extensions import Self


class AmazonScraper:
    """
    Amazon scraper to fetch reviews from products with multi-threading
    with support for logging in
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

    def _login_single(self, browser: Firefox, email: str, password: str) -> None:
        browser.get("https://amazon.com")
        try:
            browser.find_element(By.ID, "nav-link-accountList").click()
            browser.find_element(By.ID, "ap_email").send_keys(email)
            browser.find_element(By.ID, "continue").click()
            browser.find_element(By.ID, "ap_password").send_keys(password)
            browser.find_element(By.ID, "signInSubmit").click()
        except NoSuchElementException:
            self._login_single(browser, email, password)

    def login(self, email: str, password: str) -> None:
        """Log in all browsers to Amazon with an email and password"""
        with ThreadPoolExecutor() as executor:
            executor.map(
                self._login_single,
                self.browsers,
                repeat(email),
                repeat(password),
            )

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
        ctx: Optional[Any] = None,
    ) -> None:
        map_star = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

        if ctx:
            pass
            # add_script_run_ctx(threading.currentThread(), ctx)
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
                # ctx = get_script_run_ctx()
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

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if getattr(self, "display", None):
            self.display.stop()
        self.close()
