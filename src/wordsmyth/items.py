from __future__ import annotations

from typing import Literal
from dataclasses import dataclass
from enum import Enum, auto

class Flags(str, Enum):
    # sentiment flags
    POS_SENTIMENT = auto()
    """- Positive Flair sentiment
    - Positive TorchMoji sentiment"""

    NEG_SENTIMENT = auto()
    """- Negative Flair sentiment
    - Negative TorchMoji sentiment"""

    NEG_FLAIR_SENTIMENT = auto()
    """- Negative Flair sentiment"""

    NEG_MAP_SENTIMENT = auto()
    """- Negative TorchMoji sentiment"""

    EMOJIS_ARE_POSITIVE = auto()
    NEG_FLAIR_CONTRADICTING = auto()
    """- Low Flair score
    - TorchMoji produced more negative emojis than positive
    - Negative Flair sentiment"""

    NEG_MAP_CONTRADICTING = auto()
    """- Low Flair score
    - TorchMoji produced more negative emojis than positive
    - Negative TorchMoji sentiment"""

    # text-related flags
    CONTAINS_LAUGHING_EMOJI = auto()
    NEG_FLAIR_CONJUGATIONS = auto()
    """- Negative Flair sentiment
    - Text contains conjugations"""

    POS_FLAIR_CONJUGATIONS = auto()
    """- Positive Flair sentiment
    - Text contains conjugations"""


@dataclass()
class ReviewData:
    """General data about a review and its outputs"""
    content: str
    emoji: str
    emojis: list[str]
    position: int
    sentiment_flair: str
    score: float
    sentiment_map: str
    fixed_emoji: str
    matches: bool
    post_fix_status: Literal["fixed", "correct", "incorrect"]


@dataclass
class Output:
    """Output from Flair and TorchMoji"""
    sentiment: dict
    emojis: list[str]
    text: str
