"""A small debug script for downloading Amazon reviews locally

Soon to be deprecated by wordsmyth.spiders"""
import json
import time
from typing import Generator
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from tqdm import tqdm


def get_product_links(browser) -> None:
    browser.get("https://www.amazon.com/gp/bestsellers/")
    links = 0
    for _ in range(5):
        for link in browser.find_elements(By.CSS_SELECTOR, "a.a-link-normal"):
            try:
                if "product-reviews" in link.get_attribute("href"):
                    yield urlparse(link.get_attribute("href")).path.split("/")[2]
                    links += 1
            except Exception:
                break
        try:
            browser.execute_script("window.scrollBy(0,1000)")
        except Exception:
            pass
    print(f"{links} LINKS :D")


def get_sources(browser, product: str, pages: int) -> Generator[str, None, None]:
    """Gets n pages from a product with an Amazon product ID"""
    for page in tqdm(range(1, pages + 1)):
        browser.get(
            f"https://www.amazon.com/product-reviews/{product}/"
            f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        )
        time.sleep(1)
        source = browser.page_source
        yield source


def process_review_page(content) -> Generator[dict, None, None]:
    for review in content:
        row = review.select_one(".a-row")
        if row is not None:
            rating = int(
                row.select_one("i[data-hook='review-star-rating']").text.split(".")[0]
            )
            body = row.select_one("span[data-hook='review-body']").text
            yield {"reviewText": body, "overall": rating}


def thread(browser, product, pages):
    for html in get_sources(browser, product, pages):
        soup = BeautifulSoup(html, "html.parser")

        content = soup.select("div[data-hook='review']")
        for item in process_review_page(content):
            print(item)


def main(pages: int) -> None:
    """Entrypoint function for downloading"""
    output = []
    opt = Options()
    opt.add_argument("--headless")
    display = Display(visible=0, size=(800, 600))
    display.start()
    # items = list(get_product_links(browser))[:5]

    items = ["B0014C5S7S", "B0000ANHT7", "B0BBGDFH4V", "B077ZMKWVM", "B0014C5S7S"]
    browser = Firefox(options=opt, firefox_binary="/usr/bin/firefox-esr")
    with ThreadPoolExecutor(max_workers=len(items)) as executor:
        for product in items:
            print(product)
            executor.submit(thread, browser, product, pages)

        # thred = Thread(target=thread, args=[browser, product, pages])
        # thred.start()
    browser.quit()

    with open("comments.json", "w", encoding="utf-8") as fh:
        json.dump(output, fh)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="A small debug script for downloading Amazon reviews locally",
        usage="./scripts/fetch_amz.py <amazon product id> <number of pages>",
    )
    parser.add_argument(dest="pages", help="Number of pages to scrape", type=int)
    args = parser.parse_args()

    main(args.pages)
