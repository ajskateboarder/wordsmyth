"""A small debug script for downloading Amazon reviews locally"""
import json
import time
from typing import Generator

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm


def get_sources(
    product: str, pages: int, headless: bool = True
) -> Generator[str, None, None]:
    """Gets n pages from a product with an Amazon product ID"""
    opt = Options()
    if headless:
        opt.add_argument("--headless")

    browser = Firefox(options=opt)

    for page in tqdm(range(1, pages + 1)):
        browser.get(
            f"https://www.amazon.com/product-reviews/{product}/"
            f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        )
        time.sleep(1)
        source = browser.page_source
        yield source
    browser.quit()


def main(product: str, pages: int, headless: bool) -> None:
    """Entrypoint function for downloading"""
    output = []

    for html in get_sources(product, pages, headless):
        soup = BeautifulSoup(html, "html.parser")

        content = soup.select("div[data-hook='review']")
        for review in content:
            row = review.select_one(".a-row")
            if row is not None:
                rating = int(
                    row.select_one("i[data-hook='review-star-rating']").text.split(".")[
                        0
                    ]
                )
                body = row.select_one("span[data-hook='review-body']").text
                output.append({"reviewText": body, "overall": rating})

    with open("comments.json", "w", encoding="utf-8") as fh:
        json.dump(output, fh)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="A small debug script for downloading Amazon reviews locally",
        usage="./scripts/fetch_amz.py <amazon product id> <number of pages>",
    )
    parser.add_argument(dest="product_id", help="Amazon product ID")
    parser.add_argument(dest="pages", help="Number of pages to scrape", type=int)
    parser.add_argument(
        "--headful",
        help="Opens the browser as a GUI for debugging purposes",
        action="store_true",
    )
    args = parser.parse_args()

    main(args.product_id, args.pages, not args.headful)
