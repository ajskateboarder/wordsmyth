#!../venv/bin/python3
"""Fetch a LOT of Amazon product IDs and scrape ~130 reviews from each proportionally"""
from __future__ import annotations

import os
import sys
from functools import partial
from uuid import uuid4
import logging

from sqlite3worker.sqlite3worker import Sqlite3Worker

from crawling import bestsellers_reviews
from crawling.dicts import Reviews
from wordsmyth import rate


logging.basicConfig(
    format="[%(levelname)s] %(asctime)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
    # filename="something.log",
)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def process_reviews(reviews: Reviews, db: Sqlite3Worker) -> None:
    productId = reviews["productId"]
    for review in reviews["items"]:
        if review["reviewText"].strip() == "":
            return
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {productId}(text, actual, prediction, flags)"
        )

        try:
            prediction, flags = rate(
                review["reviewText"]
                .replace(
                    "                    The media could not be loaded.\n                ",
                    "",
                )
                .strip(),
                flags=True,
            )
        except Exception:
            return
        try:
            db.execute(
                f"INSERT INTO {productId} VALUES(?, ?, ?, ?)",
                (
                    review["reviewText"],
                    review["overall"],
                    prediction,
                    ",".join(flags),
                ),
            )
        except AttributeError:
            db.execute(
                f"INSERT INTO {productId} VALUES(?, ?, ?, ?)",
                (review["reviewText"], review["overall"], prediction, flags),
            )


def main() -> None:
    HEADLESS = False

    location = f"{sys.argv[1].split('.')[0]}{str(uuid4())}.sqlite"
    db = Sqlite3Worker(location)
    logging.info("Writing reviews to %s", location)

    scraper = bestsellers_reviews(partial(process_reviews, db=db), HEADLESS)
    scraper(os.environ["EMAIL"], os.environ["PASSWORD"])


if __name__ == "__main__":
    main()
