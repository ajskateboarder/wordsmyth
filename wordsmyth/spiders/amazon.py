"""Amazon scraper implementation

```
AmazonScraper().fetch_reviews(10)
```
"""
import time
from typing import Generator
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class AmazonScraper:
    """This implementation uses Firefox and Geckodriver.

    `fake_display` creates a virtual display for non-window systems.
    This requires `xvfb`"""
    def __init__(
        self, fake_display=False, location: str = "/usr/bin/firefox-esr"
    ) -> None:
        if fake_display:
            from pyvirtualdisplay import Display

            display = Display(visible=0, size=(800, 600))
            display.start()
        opt = Options()
        opt.add_argument("--headless")
        self.browser = Firefox(options=opt, firefox_binary=location)

    def get_bestselling(self) -> Generator[str, None, None]:
        """Fetch product IDs from Amazon's Bestsellers page"""
        self.browser.get("https://www.amazon.com/gp/bestsellers/")
        for _ in range(5):
            for link in self.browser.find_elements(By.CSS_SELECTOR, "a.a-link-normal"):
                try:
                    if "product-reviews" in link.get_attribute("href"):
                        yield urlparse(link.get_attribute("href")).path.split("/")[2]
                        links += 1
                except Exception:
                    break
            try:
                self.browser.execute_script("window.scrollBy(0,1000)")
            except Exception:
                pass

    def select_product_source(
        self, product: str, pages: int, delay: int = 1
    ) -> Generator[str, None, None]:
        """Fetch n pages of reviews by product ID"""
        for page in range(1, pages + 1):
            self.browser.get(
                f"https://www.amazon.com/product-reviews/{product}/"
                f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
            )
            time.sleep(delay)
            source = self.browser.page_source
            yield source

    @staticmethod
    def select_reviews(content) -> Generator[dict, None, None]:
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

    def _fetch_reviews(self, product: str, pages: int):
        for page in self.select_product_source(product, pages):
            soup = BeautifulSoup(page, "html.parser")

            content = soup.select("div[data-hook='review']")
            for item in self.select_reviews(content):
                yield item

    def fetch_reviews(
        self, pages: int
    ) -> Generator[Generator[dict, None, None], None, None]:
        """Launch a thread pool to scrape reviews."""
        items = list(self.get_bestselling())
        with ThreadPoolExecutor(max_workers=len(items)) as executor:
            futures = [
                executor.submit(self._fetch_reviews, product, pages)
                for product in items
            ]
            for future in as_completed(futures):
                yield future.result()
