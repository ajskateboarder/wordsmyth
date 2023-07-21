"""Review downloader"""
from __future__ import annotations
import itertools

import time
from typing import Generator as Generator_, Optional, Any, Union, TypeVar
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By

_T = TypeVar("_T")
Generator = Generator_[_T, None, None]


class NoLinksFound(Exception):
    """No links were found on a page"""


class BotDetected(Exception):
    """Detected by Amazon and requires a CAPTCHA to proceed"""


class AmazonScraper:
    """This implementation uses Firefox and Geckodriver.

    `fake_display` creates a virtual display for non-window systems.
    This requires `xvfb`"""

    def __init__(self, fake_display: bool = True) -> None:
        if fake_display:
            self.display = Display(visible=False, size=(800, 600))
            self.display.start()

        opts = FirefoxOptions()
        if fake_display:
            opts.add_argument("--headless")  # type: ignore

        self.browser = Firefox(options=opts)

    def get_bestselling(self) -> Generator[str]:
        """Fetch product IDs from Amazon's Bestsellers page"""
        self.browser.get("https://www.amazon.com/gp/bestsellers/")
        for _ in range(5):
            for link in self.browser.find_elements(By.CSS_SELECTOR, "a.a-link-normal"):
                try:
                    if "product-reviews" in link.get_attribute("href"):
                        yield urlparse(link.get_attribute("href")).path.split("/")[2]
                except Exception:
                    break
            try:
                self.browser.execute_script("window.scrollBy(0, 1000)")  # type: ignore
            except Exception:
                pass

    def fetch_product_reviews(self, asin: str, pages: int = 10) -> Generator[dict]:
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
    ) -> Generator[str]:
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
    def select_reviews(content: Any) -> Generator[dict]:
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
                yield {"reviewText": body, "overall": rating}

    def close(self) -> None:
        """Close the browser"""
        self.browser.quit()

    def __enter__(self) -> AmazonScraper:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if getattr(self, "display", None):
            self.display.stop()
        self.close()
