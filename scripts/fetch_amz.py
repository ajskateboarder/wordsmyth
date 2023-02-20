import json
import time

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox


def get_sources(pages):
    browser = Firefox()
    for page in range(pages):
        browser.get(
            f"https://www.amazon.com/Innate-vitality-Magnesium-Glycinate-500mg/product-reviews/B07K5WDLBG/?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        )
        time.sleep(1)
        source = browser.page_source
        yield source
    browser.quit()


def main():
    output = []

    for html in get_sources(50):
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
    main()
