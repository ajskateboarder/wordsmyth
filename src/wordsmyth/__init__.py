"""Wordsmyth - generate unbiased star ratings from user reviews and comments"""
from __future__ import annotations

import json
import warnings
from functools import lru_cache

from wordsmyth.constants import DIR_PATH
from wordsmyth.items import Flags, Output
from wordsmyth.rate import Rater


@lru_cache(maxsize=None)
def _models():
    from wordsmyth.models import Flair, TorchMoji

    return Flair(), TorchMoji()


@lru_cache(maxsize=None)
def _emojimap():
    with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
        return json.load(emojimap)


def rate(
    text: str,
    *,
    emojis: int = 10,
    rounded: bool = True,
    flags: bool = False,
) -> tuple[(int | float), list[Flags] | None]:
    """Assign a star rating to text"""
    warnings.filterwarnings("ignore")
    flair, torch = _models()
    output = Output(
        sentiment=flair.predict(text), emojis=torch.predict(text, emojis), text=text
    )

    rater = Rater(output, _emojimap())
    return rater.rate(rounded), rater.flags if flags else None
