"""Wordsmyth - generate unbiased star ratings from user reviews and comments"""
from __future__ import annotations

from functools import lru_cache
import warnings
import json

from wordsmyth.rate import Rater
from wordsmyth.items import Output, Flags
from wordsmyth.constants import DIR_PATH

CONJUGATION_SUPPORT = True
try:
    from wordsmyth.conjugation import Conjugation as _
except ImportError:
    CONJUGATION_SUPPORT = False


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
    conjugation: bool = False,
    flags: bool = False,
) -> tuple[(int | float), list[Flags] | None]:
    """Assign a star rating to text"""
    warnings.filterwarnings("ignore")
    flair, torch = _models()
    output = Output(
        sentiment=flair.predict(text), emojis=torch.predict(text, emojis), text=text
    )

    if conjugation and not CONJUGATION_SUPPORT:
        raise ImportError(
            "Conjugation detection is not supported unless the cc extra is installed"
        )

    rater = Rater(output, _emojimap())

    rater.fix_content()
    rater.flag()

    return rater.rate(rounded), rater.flags if flags else None
