"""Find a bunch of product URLs"""
from __future__ import annotations
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from .scrape import AmazonScraper


class AmazonBestsellersScraper(AmazonScraper):
    """
    Amazon scraper to find links on Bestsellers
    (https://www.amazon.com/gp/bestsellers)
    """

    def get_bestselling(self, scrolls: int = 5) -> list[str]:
        """Fetch product IDs from Amazon's Bestsellers page"""
        self.browser.get("https://www.amazon.com/gp/bestsellers/")
        results = []
        for _ in range(scrolls):
            for link in self.browser.find_elements(By.CSS_SELECTOR, "a.a-link-normal"):
                try:
                    if "product-reviews" in link.get_attribute("href"):
                        results.append(
                            urlparse(link.get_attribute("href")).path.split("/")[2]
                        )
                except Exception:  # pylint:disable=broad-exception-caught
                    break
            try:
                self.browser.execute_script("window.scrollBy(0, 1000)")  # type: ignore
            except Exception:  # pylint:disable=broad-exception-caught
                pass
        return list(set(results))

    def fetch_bestselling_reviews(
        self, pages: int, limit: Optional[int] = None
    ) -> Optional[Generator[Generator[dict]]]:
        """Launch a thread pool to scrape reviews from 'Best Sellers'"""
        if limit:
            items = list(itertools.islice(self.get_bestselling(), limit))
        else:
            items = list(self.get_bestselling())
        if len(items) == 0:
            return None
        with ThreadPoolExecutor(max_workers=len(items)) as executor:
            futures = [
                executor.submit(self.fetch_product_reviews, product, pages)
                for product in items
            ]
            return (future.result() for future in as_completed(futures))
