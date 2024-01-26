"""Review generation helpers"""
from __future__ import annotations

import logging
import subprocess
from itertools import count
from typing import TYPE_CHECKING, Any, Callable, Protocol, cast

from .sync_reviews import AmazonScraper
from .threaded_reviews import AmazonScraper as ParallelAmazonScraper

if TYPE_CHECKING:
    from selenium.webdriver import Firefox


class Scraper(Protocol):
    def __call__(self, email: str, password: str) -> None:
        ...


def kitty_captcha(browser: Firefox, _: Any) -> str:
    captcha_image = cast(
        str,
        browser.find_element("css selector", "img[alt='captcha']").get_attribute("src"),
    )
    subprocess.run(["/usr/bin/kitty", "icat", captcha_image], check=True)
    return input("(login) Please solve the provided captcha: ")


def bestsellers_reviews(callback: Callable, headless: bool) -> Scraper:
    """Returns a scraping function to scrape reviews from Amazon's bestselling"""

    def scraper(email: str, password: str) -> None:
        logging.info("Starting product ID gatherer")

        with AmazonScraper(headless) as products:
            logging.info("Collecting product IDs")
            product_ids = products.get_bestselling()
            logging.info(
                "Collected %s following IDs: %s",
                len(product_ids),
                ",".join(product_ids),
            )

        logging.info("Initializing review gatherer")

        with AmazonScraper(headless) as prop:
            with ParallelAmazonScraper(headless) as scrapers:
                scrapers.captcha_hook = kitty_captcha
                logging.info("Logging scrapers in")
                scrapers.login(email, password)
                for i in count(1):
                    logging.info("Starting round %s of scraping", i)
                    for product_id in product_ids[:]:
                        logging.info("Initiating scrape process for: %s", product_id)
                        logging.info("\tCollecting review proportions")
                        data = prop.get_extras(product_id)
                        logging.info(
                            "Collected %s following IDs: %s",
                            len(data.products),
                            ",".join(data.products),
                        )
                        logging.info("\tScraping")
                        scrapers.scrape(product_id, callback, data.proportions)  # type: ignore

                        product_ids.extend(data.products)
                        product_ids.remove(product_id)

    return scraper
