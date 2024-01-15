"""Amazon review collection utilities"""
from .ids import BestSellersLinks
from .sync_reviews import AmazonScraper
from .threaded_reviews import AmazonScraper as ParallelAmazonScraper
