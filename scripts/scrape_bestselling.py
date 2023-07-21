"""Fetch a LOT of Amazon product IDs and scrape ~130 reviews from each proportionally"""
import csv

import amazon_utils as utils
from wordsmyth import Pipeline

pipe = Pipeline()


def process_review(review: dict) -> None:
    with open(
        f"data/{review['productId']}.csv", "a+", encoding="utf-8", newline=""
    ) as csvfile:
        columns = ["reviewText", "overall", "predicted_rating", "productId"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)

        # TODO: mitigate excessive IO work
        with open(f"data/{review['productId']}.csv", encoding="utf-8") as csvread:
            try:
                csvread.readlines()[0]
            except Exception:
                writer.writeheader()

        try:
            prediction = pipe.predict(review["reviewText"])
        except AssertionError:
            prediction = "assertion_error"

        writer.writerow({**review, "predicted_rating": prediction})


def main() -> None:
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
            scrapers.scrape(product_id, process_review, proportions)  # type: ignore


if __name__ == "__main__":
    main()
