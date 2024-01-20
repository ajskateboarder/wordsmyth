"""Review downloader

Used in review aggregating to find popular products"""
from __future__ import annotations

import time
from typing import Any, Generator, Union, cast
from urllib.parse import urlparse
from urllib3.exceptions import MaxRetryError

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By

from .dicts import Review
from .exceptions import PrematureBrowserExit


class AmazonScraper:
    """This implementation uses Firefox and Geckodriver.

    `fake_display` creates a virtual display for non-window systems."""

    def __init__(self, fake_display: bool = True) -> None:
        opts = FirefoxOptions()
        if fake_display:
            opts.add_argument("--headless")  # type: ignore

        self.browser = Firefox(options=opts)

    def __enter__(self) -> AmazonScraper:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def get_bestselling(self) -> list[str]:
        """Fetch product IDs from Amazon's Bestsellers page"""
        try:
            self.browser.get("https://www.amazon.com/gp/bestsellers/")
        except MaxRetryError as e:
            raise PrematureBrowserExit(
                "Failed to access a browser session. Did you format your 'with' blocks correctly?"
            ) from e
        ids = []
        for _ in range(3):
            for link in self.browser.find_elements(By.CSS_SELECTOR, "a.a-link-normal"):
                try:
                    if "product-reviews" not in cast(str, link.get_attribute("href")):
                        continue
                    product_id = cast(
                        str, urlparse(link.get_attribute("href")).path
                    ).split("/")[2]
                    ids.append(product_id)
                except Exception:
                    break
            try:
                self.browser.execute_script("window.scrollBy(0, 1000)")  # type: ignore
            except Exception:
                pass
        return list(set(ids))

    def fetch_product_reviews(
        self, asin: str, pages: int = 10
    ) -> Generator[dict, None, None]:
        """Fetch reviews from a single product ASIN"""
        for page in self.get_product_source(asin, pages):
            soup = BeautifulSoup(page, "html.parser")

            content = soup.select("div[data-hook='review']")
            for item in self.select_reviews(content):
                yield {**item, "productId": asin}

    def get_proportions(
        self, asin: str, total: int = 500
    ) -> Union[list[float], list[int]]:
        """Return the distribution of reviews to gather from five to one star

        If `total` is None, return the percentages from a product histogram as floats"""
        self.browser.get(f"https://amazon.com/product-reviews/{asin}")

        percentages = self.browser.find_element(
            By.CSS_SELECTOR, ".histogram"
        ).text.split("\n")[1::2]
        parsed = list(map(lambda p: int(p.replace("%", "")) / 100, percentages))
        if total is None:
            return parsed
        parsed = list(map(lambda x: x * 500, parsed))
        while any(x > 100 for x in parsed):
            parsed = list(map(lambda x: x * 0.99, parsed))
        return list(reversed(list(map(lambda x: int(x) + 1, parsed))))

    def get_product_source(
        self, asin: str, pages: int, delay: float = 0.5
    ) -> Generator[str, None, None]:
        """Fetch n pages of reviews by product ID"""
        for page in range(1, pages + 1):
            self.browser.get(
                f"https://www.amazon.com/product-reviews/{asin}/"
                f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
            )
            time.sleep(delay)
            source = self.browser.page_source
            yield source

    @staticmethod
    def select_reviews(content: Any) -> Generator[Review, None, None]:
        """Select reviews from an Amazon page source"""
        for review in content:
            row = review.select_one(".a-row")
            if row is not None:
                rating = int(
                    row.select_one("i[data-hook='review-star-rating']").text.split(".")[
                        0
                    ]
                )
                body = row.select_one("span[data-hook='review-body']").text
                yield {"text": body, "rating": rating}

    def close(self) -> None:
        """Close the browser"""
        self.browser.quit()
