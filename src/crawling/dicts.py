"""Typings for some JSON structures"""
from __future__ import annotations
from typing import TypedDict


class Review(TypedDict):
    text: str
    rating: int


class Reviews(TypedDict):
    productId: str
    items: list[Review]


class Product(TypedDict):
    title: str
    asin: str
    rating: str
    price: str
    image: str
