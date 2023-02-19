from __future__ import annotations
from typing import Any, Literal, Optional
from dataclasses import dataclass


@dataclass
class Sentiment:
    flair: str
    map: str


@dataclass
class Item:
    content: str
    emoji: dict[str, Any]
    position: int
    sentiment: Sentiment
    emojis: list[str]
    matches: bool
    score: float
    status: Literal["incorrect", "correct", "fixed"]
    fixed: Optional[str] = None

    def __post_init__(self):
        self.sentiment = Sentiment(**self.sentiment)
