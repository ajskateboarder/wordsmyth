from __future__ import annotations

import json
import attrs

from .constants import DIR_PATH
from .rate_utils import fix_content, rate


@attrs.define
class Sentiment:
    """Represents Flair sentiment output"""
    sentiment: str
    score: float


@attrs.define
class Output:
    """Represents output from Pipeline.eval"""
    sentiment: Sentiment
    emojis: list[str]
    text: str

    def rating(self):
        """Rate text using data from Flair `en-sentiment` and TorchMoji"""
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            rate_map = json.load(emojimap)
        fixed = self._fix_content()
        return rate(fixed, rate_map)

    def _fix_content(self):
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            fix_map = {e["repr"]: e for e in json.load(emojimap)}
            fix_map[":cry:"]["sentiment"] = "neg"
            fix_map[":grimacing:"]["sentiment"] = "neu"
        return fix_content(attrs.asdict(self), fix_map)
