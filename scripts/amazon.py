"""
Product indexer/review downloader
Bulk-request reviews and dump them to a JSON file
"""
import argparse
import sys
import json
import itertools
import logging

import time
from typing import Generator, Optional, Any, AsyncGenerator
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By


class NoLinksFound(Exception):
    """No links were found on a page"""


class BotDetected(Exception):
    """Detected by Amazon and requires a CAPTCHA to proceed"""


class AmazonScraper:
    """This implementation uses Firefox and Geckodriver.

    `fake_display` creates a virtual display for non-window systems.
    This requires `xvfb`"""

    def __init__(
        self, fake_display: bool = True, location: str = "/usr/bin/firefox-esr"
    ) -> None:
        if fake_display:
            display = Display(visible=False, size=(800, 600))
            display.start()

        try:
            self.browser = Firefox(firefox_binary=location)
        except TypeError:
            # unexpected keyword argument 'firefox_binary'
            self.browser = Firefox()

    def login(self, email: str, password: str) -> bool:
        """Log the scraper into Amazon with a username and password
        so reviews can be filtered

        Amazon will likely detect the bot after a couple of scrapes,
        so you will have to launch the script in headful mode to solve CAPTCHAs.
        From there, Amazon will trust your public IP.
        """
        self.browser.get("https://amazon.com")
        time.sleep(0.3)
        try:
            self.browser.find_element(By.ID, "nav-link-accountList").click()
            time.sleep(0.3)
            self.browser.find_element(By.ID, "ap_email").send_keys(email)
            self.browser.find_element(By.ID, "continue").click()
            time.sleep(0.3)
            self.browser.find_element(By.ID, "ap_password").send_keys(password)
            self.browser.find_element(By.ID, "signInSubmit").click()
            time.sleep(0.3)
        except Exception:
            self.login(email, password)

        if (
            "ap/cvf/request" in self.browser.current_url
            or self.browser.current_url == "https://www.amazon.com/ap/signin"
        ):
            raise BotDetected(
                "Solve the CAPTCHA manually by running AmazonScraper with fake_display=False"
            )

        return True

    def get_bestselling(self) -> Generator[str, None, None]:
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

    def get_product_source(
        self, asin: str, pages: int, sort_by: int, delay: float = 0.5
    ) -> Generator[str, None, None]:
        """Fetch n pages of reviews by product ID"""
        map_star = {
            1: "one_star",
            2: "two_star",
            3: "three_star",
            4: "four_star",
            5: "five_star",
        }
        for page in range(1, pages + 1):
            self.browser.get(
                f"https://www.amazon.com/product-reviews/{asin}/"
                f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page}&filterByStar={map_star[sort_by]}"
            )
            time.sleep(delay)
            source = self.browser.page_source
            yield source

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
                yield {"reviewText": body, "overall": rating}

    def fetch_product_reviews(
        self, asin: str, sort_by: int, pages: int = 10
    ) -> Generator[dict, None, None]:
        """Fetch reviews from a single product ASIN"""
        for page in self.get_product_source(asin, pages, sort_by):
            soup = BeautifulSoup(page, "html.parser")

            content = soup.select("div[data-hook='review']")
            for item in self.select_reviews(content):
                yield {**item, "productId": asin}

    async def thread_fetch_reviews(
        self, asin: str, pages: int = 10
    ) -> AsyncGenerator[dict, None]:
        """Scrape reviews available on an Amazon product (max: 500)

        `pages` is a maximum of 10 since reviews beyond page 11 are not accessible"""
        if pages > 10:
            raise Exception("pages beyond 10 are not allowed by Amazon")

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.fetch_product_reviews, asin, i, pages)
                for i in range(1, 6)
            ]
            for future in as_completed(futures):
                for result in future.result():
                    yield result

    def fetch_bestselling_reviews(
        self, pages: int, limit: Optional[int] = None, *, log: bool = False
    ) -> Generator[Generator[dict, None, None], None, None]:
        """Launch a thread pool to scrape reviews from 'Best Sellers'"""
        if limit:
            items = list(itertools.islice(self.get_bestselling(), limit))
        else:
            items = list(self.get_bestselling())
        if len(items) == 0:
            raise NoLinksFound()
        if log:
            logging.info(
                "Fetching %s pages of reviews from %s products (%s). Press Ctrl+C to stop at any time",
                pages,
                len(items),
                len(items) * pages * 10,
            )
        with ThreadPoolExecutor(max_workers=len(items)) as executor:
            futures = [
                executor.submit(self.fetch_product_reviews, product, pages)
                for product in items
            ]
            for future in as_completed(futures):
                yield future.result()


def main() -> None:
    """Entrypoint to command line"""
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Streams Amazon product reviews as JSON lines format (.jsonl)"
    )
    parser.add_argument(
        "pages", type=int, help="Number of pages to scrape from each product"
    )
    parser.add_argument(
        "--no-fake-display",
        action="store_false",
        help="Disables fake display for usage on non-window systems. "
        "Enabled by default because it is compatible with window systems",
    )
    parser.add_argument(
        "--products",
        type=int,
        help="Limits the number of bestseller products to scrape from.",
    )
    parser.add_argument(
        "--use-esr",
        action="store_true",
        help="Use /usr/bin/firefox-esr for screen scraping. "
        "This is usually where Firefox is located on Debian",
    )

    args = parser.parse_args()

    scraper = AmazonScraper(
        args.no_fake_display,
        location="/usr/bin/firefox-esr" if args.use_esr else "/usr/bin/firefox",
    )

    def _try_scrape() -> None:
        for product in scraper.fetch_reviews(args.pages, args.products, log=True):
            for review in product:
                print(json.dumps(review))

    logging.info("Scraping product links on https://amazon.com/gp/bestsellers")
    try:
        _try_scrape()
    except NoLinksFound:
        logging.warning("Product link scraping failed. Retrying...")
        _try_scrape()


if __name__ == "__main__":
    main()
