from __future__ import annotations
from typing import Optional, Any
from dataclasses import dataclass

import json

from wordsmyth.constants import DIR_PATH
from wordsmyth.rate_utils import fix_content, rate


class Int(int):
    def __new__(cls, value: int | str, metadata: Optional[dict] = None) -> Int:
        obj = int.__new__(cls, value)
        obj.metadata = metadata
        cls.metadata = metadata
        return obj


class Float(float):
    def __new__(cls, value: float | str, metadata: Optional[dict] = None) -> Float:
        obj = int.__new__(cls, value)
        obj.metadata = metadata
        cls.metadata = metadata
        return obj


@dataclass
class Sentiment:
    """Represents Flair sentiment output"""

    sentiment: str
    score: float


@dataclass
class Output:
    """Represents output from Pipeline.eval"""

    sentiment: Sentiment
    emojis: list[str]
    text: str

    def rating(self, exact: bool = True) -> Optional[Int | Float]:
        """Rate text using data from Flair `en-sentiment` and TorchMoji"""
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            rate_map = json.load(emojimap)
        fixed = self._fix_content()
        rating = rate(fixed, rate_map)  # type: ignore
        return (
            Int(round(min(5, rating * 10)), fixed)  # type: ignore
            if not exact
            else rating  # type: ignore
        )

    def _fix_content(self) -> Optional[dict[str, Any]]:
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            fix_map = {e["repr"]: e for e in json.load(emojimap)}
            fix_map[":cry:"]["sentiment"] = "neg"
            fix_map[":grimacing:"]["sentiment"] = "neu"
        return fix_content(self, fix_map)
