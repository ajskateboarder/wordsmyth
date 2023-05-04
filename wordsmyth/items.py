from __future__ import annotations

import json
from typing import Literal, Any, Optional, Union

import attrs

from .constants import DIR_PATH
from .rate_utils import fix_content, rate


@attrs.define
class Sentiment:
    sentiment: Literal["pos", "neu", "neg"]
    score: float


@attrs.define
class Output:
    sentiment: Sentiment
    emojis: list[str]
    text: str

    def rate(self) -> Union[int, float]:
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            rate_map = json.load(emojimap)
        fixed = self._fix_content()
        return rate(fixed, rate_map)  # type: ignore

    def _fix_content(self) -> Optional[dict[str, Any]]:
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            fix_map = {e["repr"]: e for e in json.load(emojimap)}
            fix_map[":cry:"]["sentiment"] = "neg"
            fix_map[":grimacing:"]["sentiment"] = "neu"
        return fix_content(attrs.asdict(self), fix_map)
