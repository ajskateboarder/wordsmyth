from crawlers.amazon import AmazonScraper

scraper = AmazonScraper(True, "/usr/bin/firefox")
for product in scraper.fetch_reviews(2):
    for review in product:
        print(review)
