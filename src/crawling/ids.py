"""Find a bunch of product URLs"""
from __future__ import annotations

from typing import Optional, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote_plus
import itertools

from typing_extensions import Self

import requests
from selenium.webdriver.common.by import By
from .reviews import AmazonScraper


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

    def _get_ids(self, url: str, scrolls: int = 1, to_rust: bool = False) -> list[dict]:
        """Fetch product IDs given a URL"""
        self.browser.get(url)

        y_scroll = 1000
        for _ in range(scrolls):
            try:
                self.browser.execute_script(f"window.scrollBy({y_scroll - 1000}, {y_scroll})")  # type: ignore
                y_scroll += 1000
            except Exception:  # pylint:disable=broad-exception-caught
                pass

        if to_rust:
            return self.browser.page_source

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
                {
                    "title": datum.text,
                    "asin": find_asin(datum.get_attribute("href")),
                    "rating": product.find_element(
                        By.CSS_SELECTOR, ".a-row.a-size-small span"
                    ).get_attribute("aria-label"),
                    "price": product.find_element(
                        By.CSS_SELECTOR, ".a-price"
                    ).text.replace("\n", "."),
                    "image": product.find_element(
                        By.CSS_SELECTOR, ".s-image"
                    ).get_attribute("src"),
                }
            )

        return items

    def get_bestsellers_ids(self, scrolls: int = 1) -> list[dict]:
        """Fetch product IDs from Amazon's Bestsellers page"""
        return self._get_ids("https://www.amazon.com/gp/bestsellers/", scrolls)

    def get_query_ids(
        self, query: str, scrolls: int = 1, to_rust: bool = False
    ) -> list[dict]:
        """Fetch product IDs from a Amazon search query"""
        return self._get_ids(
            f"https://amazon.com/s?k={quote_plus(query)}", scrolls, to_rust
        )

    def fetch_bestselling_reviews(
        self, pages: int, limit: Optional[int] = None
    ) -> Optional[Generator[Generator[dict, None, None], None, None]]:
        """Launch a thread pool to scrape reviews from products on 'Best Sellers'"""
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

    def __enter__(self) -> Self:
        return self


def suggestions(query: str) -> list[str]:
    """Give product completions from a query"""
    res = requests.get(
        "https://completion.amazon.com/api/2017/suggestions"
        f"?limit=11&prefix={query}&suggestion-type=WIDGET&suggestion-type=KEYWORD"
        "&page-type=Gateway&alias=aps&site-variant=desktop&version=3&wc=&lop=en_US&fb=1&plain-mid=1&client-info=amazon-search-ui",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
            "Origin": "https://www.amazon.com",
            "Referer": "https://www.amazon.com/",
        },
        timeout=10,
    ).json()
    return [s["value"] for s in res["suggestions"]]
