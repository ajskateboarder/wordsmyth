"""Find a bunch of product URLs"""
from __future__ import annotations

from typing import Any, cast
from urllib.parse import quote_plus

from selenium.webdriver.common.by import By
from typing_extensions import Self

from .sync_reviews import AmazonScraper
from .dicts import Product


def find_asin(url: str) -> str:
    """Find a product ASIN in a URL"""
    path = url.split("/")
    if "?" in path[-1]:
        return path[-2]
    if not path[0] == "https:":
        return url
    return path[-1]


class BestSellersLinks(AmazonScraper):
    """
    Amazon scraper to find links on Best sellers
    (https://www.amazon.com/gp/bestsellers)
    """

    def _get_ids(self, url: str, scrolls: int = 1) -> list[Product]:
        """Fetch product IDs from a given URL"""
        self.browser.get(url)

        y_scroll = 1000
        for _ in range(scrolls):
            try:
                self.browser.execute_script(f"window.scrollBy({y_scroll - 1000}, {y_scroll})")  # type: ignore
                y_scroll += 1000
            except Exception:  # pylint:disable=broad-exception-caught
                pass

        items = []
        for product in self.browser.find_elements(
            By.CSS_SELECTOR, "div[class=a-section]"
        )[:-1]:
            datum = product.find_elements(By.CSS_SELECTOR, "a")[1]
            if datum.text == "Sponsored":
                continue
            if datum.text == "":
                datum = list(
                    filter(
                        lambda x: x.text != "",
                        product.find_elements(By.CSS_SELECTOR, "a"),
                    )
                )[1]
            items.append(
                cast(
                    Product,
                    {
                        "title": datum.text,
                        "asin": find_asin(cast(str, datum.get_attribute("href"))),
                        "rating": product.find_element(
                            By.CSS_SELECTOR, ".a-row.a-size-small span"
                        ).get_attribute("aria-label"),
                        "price": product.find_element(
                            By.CSS_SELECTOR, ".a-price"
                        ).text.replace("\n", "."),
                        "image": product.find_element(
                            By.CSS_SELECTOR, ".s-image"
                        ).get_attribute("src"),
                    },
                )
            )

        return items

    def get_bestsellers_ids(self, scrolls: int = 1) -> list[Product]:
        """Fetch product IDs from Amazon's Bestsellers page"""
        return self._get_ids("https://www.amazon.com/gp/bestsellers/", scrolls)

    def get_query_ids(self, query: str, scrolls: int = 1) -> list[Product]:
        """Fetch product IDs from a Amazon search query"""
        return self._get_ids(f"https://amazon.com/s?k={quote_plus(query)}", scrolls)
