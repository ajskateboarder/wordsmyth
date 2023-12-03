from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal


class Flags(str, Enum):
    # sentiment flags
    POS_SENTIMENT = auto()
    NEG_SENTIMENT = auto()
    NEG_FLAIR_SENTIMENT = auto()
    NEG_MAP_SENTIMENT = auto()
    EMOJIS_ARE_POSITIVE = auto()
    NEG_FLAIR_CONTRADICTING = auto()
    NEG_MAP_CONTRADICTING = auto()
    CONTAINS_LAUGHING_EMOJI = auto()
    NEG_FLAIR_CONJUGATIONS = auto()
    POS_FLAIR_CONJUGATIONS = auto()


@dataclass()
class Evaluation:
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
