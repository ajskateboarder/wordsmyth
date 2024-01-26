"""Typings for some JSON structures"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Review:
    text: str
    rating: int


@dataclass
class Reviews:
    product_id: str
    items: list[Review]


@dataclass
class Product:
    title: str
    asin: str
    rating: str
    price: str
    image: str


@dataclass
class ProductPageInfo:
    proportions: list[float] | list[int]
    products: list[str]
