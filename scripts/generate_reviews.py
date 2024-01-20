#!../venv/bin/python3
"""Fetch a LOT of Amazon product IDs and scrape ~130 reviews from each proportionally"""
from __future__ import annotations

import os
import sqlite3
import sys
from functools import partial
from threading import Lock
import logging

from crawling import bestsellers_reviews
from crawling.dicts import Reviews

from wordsmyth import rate

lock = Lock()

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


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

    def __exit__(self, *_) -> None:
        self.lock.release()
        self.connection.commit()
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None  # type: ignore


def process_reviews(reviews: Reviews, db: LockedSqliteConnection) -> None:
    productId = reviews["productId"]
    with lock:
        for review in reviews["items"]:
            if review["reviewText"].strip() == "":
                return
            with db:
                db.cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {productId}(text, actual, prediction, flags)"
                )

                try:
                    prediction, flags = rate(
                        review["reviewText"]
                        .replace(
                            "                    The media could not be loaded.\n                ",
                            "",
                        )
                        .strip()
                    )
                except Exception:
                    return
                try:
                    db.cursor.execute(
                        f"INSERT INTO {productId} VALUES(?, ?, ?, ?)",
                        (
                            review["reviewText"],
                            review["overall"],
                            prediction,
                            ",".join(flags),
                        ),
                    )
                except AttributeError:
                    db.cursor = db.connection.cursor()
                    db.cursor.execute(
                        f"INSERT INTO {productId} VALUES(?, ?, ?)",
                        (review["reviewText"], review["overall"], prediction),
                    )


def main() -> None:
    HEADLESS = False

    db = LockedSqliteConnection(sys.argv[1])

    scraper = bestsellers_reviews(partial(process_reviews, db=db), HEADLESS)
    scraper(os.environ["EMAIL"], os.environ["PASSWORD"])


if __name__ == "__main__":
    main()
