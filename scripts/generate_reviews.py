#!../venv/bin/python3
"""Fetch a LOT of Amazon product IDs and scrape ~130 reviews from each proportionally"""
from __future__ import annotations

import os
import sys
from math import inf
from uuid import uuid4
import logging

from sqlite3worker.sqlite3worker import Sqlite3Worker

from crawling import bestsellers_reviews
from crawling.items import Reviews
from wordsmyth import rate


def process_reviews(reviews: Reviews, db: Sqlite3Worker) -> None:
    product_id = reviews.product_id
    for review in reviews.items:
        if review.text.strip() == "":
            return
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {product_id}(text, actual, prediction, flags)"
        )

        try:
            prediction, flags = rate(
                review.text.replace(
                    "                    The media could not be loaded.\n                ",
                    "",
                ).strip(),
                flags=True,
            )
        except Exception as e:
            logging.error(
                "Exception raised when attempting to rate %s: %s", review.text, e
            )
            return
        try:
            db.execute(
                f"INSERT INTO {product_id} VALUES(?, ?, ?, ?)",
                (
                    review.text,
                    review.rating,
                    prediction,
                    ",".join(flags),
                ),
            )
        except AttributeError:
            db.execute(
                f"INSERT INTO {product_id} VALUES(?, ?, ?, ?)",
                (review.text, review.rating, prediction, flags),
            )


def main() -> None:
    HEADLESS = True

    location = f"{sys.argv[1].split('.')[0]}{str(uuid4())}.sqlite"

    logging.basicConfig(
        format="[%(levelname)s] %(asctime)s: %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.DEBUG,
        filename=f"{location}.log",
    )
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    db = Sqlite3Worker(location, max_queue_size=inf)
    print(f"Writing reviews to {location} and logging at {location + '.log'}")
    print("CTRL+C to exit at any time")

    scraper = bestsellers_reviews(lambda x: process_reviews(x, db), HEADLESS)
    try:
        scraper(os.environ["EMAIL"], os.environ["PASSWORD"])
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
