#!../venv/bin/python3
"""Fetch a LOT of Amazon product IDs and scrape ~130 reviews from each proportionally"""
from __future__ import annotations
from typing import Optional

from functools import partial
from threading import Lock
import sqlite3

from wordsmyth import Pipeline
from wordsmyth import scraping as utils

pipe = Pipeline()


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

        prediction = pipe.predict(review["reviewText"])
        db.cursor.execute(
            f"INSERT INTO {name} VALUES(?, ?, ?)",
            (review["reviewText"], review["overall"], prediction),
        )


def main() -> None:
    db = LockedSqliteConnection("reviews.sqlite")
    with utils.ParallelAmazonScraper() as scrapers:
        print("logging scrapers in")
        scrapers.login("the.mystic.6660@gmail.com", "adiiscool74@")
        with utils.AmazonBestsellersScraper() as products:
            print("collecting product ids")
            product_ids = products.get_bestselling()
        for product_id in product_ids:
            print("collecting proportions for:", product_id)
            with utils.AmazonScraper() as scraper:
                proportions = scraper.get_proportions(product_id)
            print("scraping:", product_id)
            scrapers.scrape(product_id, partial(process_review, db=db), proportions)  # type: ignore


if __name__ == "__main__":
    main()
