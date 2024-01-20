from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Flags(str, Enum):
    """Flags used for rule-based portion of rating"""

    POS_SENTIMENT = "pos_sentiment"
    NEG_SENTIMENT = "neg_sentiment"
    NEG_FLAIR_SENTIMENT = "neg_flair_sentiment"
    NEG_MAP_SENTIMENT = "neg_map_sentiment"
    EMOJIS_ARE_POSITIVE = "any_emojis_are_positive"
    NEG_FLAIR_CONTRADICTING = "neg_flair_and_contradicting"
    NEG_MAP_CONTRADICTING = "neg_map_and_contradicting"
    CONTAINS_LAUGHING_EMOJI = "contains_laughing_emoji"  # pretty rare for most content
    NEG_FLAIR_CONJUGATIONS = "neg_flair_and_conjugations"
    POS_FLAIR_CONJUGATIONS = "pos_flair_and_conjugations"


@dataclass
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
