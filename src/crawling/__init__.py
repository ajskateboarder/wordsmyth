"""Amazon review collection utilities"""
from .ids import BestSellersLinks
from .threaded_reviews import AmazonScraper as ParallelAmazonScraper
from .sync_reviews import AmazonScraper
