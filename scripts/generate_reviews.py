#!../venv/bin/python3
"""Fetch a LOT of Amazon product IDs and scrape ~130 reviews from each proportionally"""
from __future__ import annotations

import os
import sqlite3
import sys
from functools import partial
from threading import Lock

from wordsmyth import rate
import crawling as utils


class LockedSqliteConnection:
    """https://stackoverflow.com/a/41206801"""

    def __init__(self, dburi: str) -> None:
        self.lock = Lock()
        self.connection = sqlite3.connect(dburi, check_same_thread=False)
        self.cursor: sqlite3.Cursor = None  # type: ignore

    def __enter__(self) -> LockedSqliteConnection:
        self.lock.acquire()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, typ, value, traceback) -> None:
        self.lock.release()
        self.connection.commit()
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None  # type: ignore


def process_review(review: dict, db: LockedSqliteConnection) -> None:
    if review["reviewText"].strip() == "":
        return
    with db:
        name = review["productId"]
        db.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {name}(text, actual, prediction)"
        )

        try:
            prediction, _ = rate(
                review["reviewText"]
                .replace(
                    "                    The media could not be loaded.\n                ",
                    "",
                )
                .strip()
            )
        except Exception:
            return
        db.cursor.execute(
            f"INSERT INTO {name} VALUES(?, ?, ?)",
            (review["reviewText"], review["overall"], prediction),
        )


def main() -> None:
    import logging

    HEADLESS = True

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f"{sys.argv[1]}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    db = LockedSqliteConnection(sys.argv[1])
    with utils.BestSellersLinks(HEADLESS) as products:
        logging.info("collecting product ids")
        product_ids = list(products.get_bestselling())
    with utils.ParallelAmazonScraper(HEADLESS) as scrapers:
        print("logging scrapers in")
        scrapers.login(os.environ["EMAIL"], os.environ["PASSWORD"])
        with utils.AmazonScraper(HEADLESS) as scraper:
            for product_id in product_ids:
                logging.info("collecting proportions for: %s", product_id)
                proportions = scraper.get_proportions(product_id)
                logging.info("scraping: %s", product_id)
                scrapers.scrape(product_id, partial(process_review, db=db), proportions)  # type: ignore


if __name__ == "__main__":
    main()
