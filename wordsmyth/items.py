from typing import Any
from dataclasses import dataclass

@dataclass
class Sentiment:
    flair: str
    map: str

@dataclass
class Item:
    content: str
    emoji: "dict[str, Any]"
    position: int
    sentiment: Sentiment
