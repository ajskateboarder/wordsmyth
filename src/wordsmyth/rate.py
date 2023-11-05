"""The flagging and rating algorithm"""

from __future__ import annotations
from typing import Any

import numpy as np

from wordsmyth.items import Output, ReviewData, Flags

class ReviewRater:
    """Assign a more accurate emoji to some text from TorchMoji output
    given Flair predictions and an emojimap.

    - `sentiment_data` is a combination of predictions from TorchMoji and Flair results
    (https://kt.ijs.si/data/Emoji_sentiment_ranking/index.html)
    - `emojimap` is a mapping of emojis to their floating-point sentiment values in negativity,
        neutrality, and positivity"""

    def __init__(self, sentiment_data: Output, emojimap: list[dict]) -> None:
        self.sentiment_data = sentiment_data
        self.metadata = ReviewData(
            content=sentiment_data.text,
            emoji=None,  # type: ignore
            emojis=sentiment_data.emojis,
            position=None,  # type: ignore
            sentiment_flair=sentiment_data.sentiment["sentiment"],
            score=sentiment_data.sentiment["score"],
            sentiment_map=None,  # type: ignore
            fixed_emoji=None,  # type: ignore
            matches=None,  # type: ignore
            post_fix_status=None,  # type: ignore
        )
        self.flags: list[Flags] = []

        self.fix_map: dict[str, dict] = {e["repr"]: e for e in emojimap}
        self.fix_map[":cry:"]["sentiment"] = "neg"
        self.fix_map[":grimacing:"]["sentiment"] = "neu"
        self.rate_map = [value for key, value in self.fix_map.items()]

    @staticmethod
    def find_indices(content: list[str], classes: list[str]) -> list[int]:
        """Find indices of list items found in classes"""
        occurences = [e in content for e in classes]
        indices = [i for i, x in enumerate(occurences) if x is True]
        return [content.index(classes[i]) for i in indices]

    def fix_content(self) -> None:
        """
        Attempt to fix Torchmoji responses by providing a better emoji built on Flair's responses.

        This is done since Flair is usually better at predicting emotions than TorchMoji,
        so this nudges TorchMoji in a better direction, I guess
        """
        m = self.metadata
        emojimap: dict = self.fix_map

        target_emojis = [":confused:", ":thumbsup:", ":eyes:", ":smile:", ":persevere:"]
        emoji_indices = self.find_indices(self.sentiment_data.emojis, target_emojis)

        try:
            first_index = min(emoji_indices)
        except ValueError:
            return

        first_emoji = self.sentiment_data.emojis[first_index]
        matched = emojimap[first_emoji]

        m.emoji = first_emoji
        m.position = first_index
        m.sentiment_map = matched["sentiment"]
        m.matches = m.sentiment_flair == matched["sentiment"]

        if m.sentiment_flair != m.sentiment_map:
            matching = [
                e
                for e in m.emojis
                if emojimap[e]["sentiment"] == m.sentiment_flair
                and emojimap[e]["repr"] in m.emojis
            ]

            # Find the index of the closest match
            sequence = [m.emojis.index(emojimap[e]["repr"]) for e in matching]
            closest_index = min(sequence) if sequence else None

            fixed = (
                emojimap.get(m.emojis[closest_index], {})
                if closest_index is not None
                else {}
            )

            if m.sentiment_flair == fixed.get("sentiment"):
                m.fixed_emoji = fixed.get("repr")
                # return here

            matching_emojis = [emojimap[emoji] for emoji in m.emojis]

            if [e["sentiment"] == "pos" for e in matching_emojis].count(True) > [
                e["sentiment"] == "neg" for e in matching_emojis
            ].count(True):
                m.sentiment_map = "pos"
            else:
                m.sentiment_map = "neg"

            target_emojis.remove(m.emoji)
            try:
                m = emojimap[
                    [
                        e
                        for e in m.emojis
                        if emojimap[e]["sentiment"] == m.sentiment_flair
                    ][0]
                ]["repr"]
            except IndexError:
                m.post_fix_status = "incorrect"

            m.post_fix_status = "fixed"

        m.post_fix_status = "correct"

    def flag(self) -> None:
        """Flags reviews based on factors for rating"""
        m = self.metadata
        emojimap = self.rate_map

        emojis_are_positive = [
            e["repr"] in m.emojis
            for e in [e for e in emojimap if e["sentiment"] == "pos"]
        ]
        emojis_are_negative = [
            e["repr"] in m.emojis
            for e in [e for e in emojimap if e["sentiment"] == "neg"]
        ]
        conjunctions = ["but", "although", "however"]
        contradicting = m.score < 0.8 and emojis_are_negative.count(
            True
        ) < emojis_are_positive.count(True)
        has_conjugations = (
            any(word in m.content.lower().strip() for word in conjunctions)
            and not contradicting
        )

        conditions = [
            (Flags.NEG_FLAIR_SENTIMENT, m.sentiment_flair == "neg"),
            (Flags.NEG_MAP_SENTIMENT, m.sentiment_map == "neg"),
            (
                Flags.POS_SENTIMENT,
                m.sentiment_map == "pos" and m.sentiment_flair == "pos",
            ),
            (
                Flags.CONTAINS_LAUGHING_EMOJI,
                "🤣" in m.content,
            ),  # this one is rather rare
            (Flags.EMOJIS_ARE_POSITIVE, any(emojis_are_positive)),
            (
                Flags.NEG_SENTIMENT,
                m.sentiment_map == "neg" and m.sentiment_flair == "neg",
            ),
            (
                Flags.NEG_FLAIR_CONTRADICTING,
                contradicting and m.sentiment_flair == "neg",
            ),
            (Flags.NEG_MAP_CONTRADICTING, contradicting and m.sentiment_map == "neg"),
            (
                Flags.NEG_FLAIR_CONJUGATIONS,
                has_conjugations and m.sentiment_flair == "neg",
            ),
            (
                Flags.POS_FLAIR_CONJUGATIONS,
                has_conjugations and m.sentiment_flair == "pos",
            ),
        ]

        self.flags = [flag for flag, condition in conditions if condition]

    def rate(self, rounded: bool = True) -> int | float:
        """Rate content using provided flags"""
        m = self.metadata

        emoji_repr = m.fixed_emoji or m.emoji or m.emojis[0]
        picked = [e for e in self.rate_map if e["repr"] == emoji_repr][0]
        negativity_score: float = np.mean(  # type: ignore
            [float(picked["pos"]), float(picked["neu"]), float(picked["neg"])]
        )

        def _match(var: Flags, cases: dict) -> Any:
            return next(value for key, value in cases.items() if key == var)

        for flag in self.flags:
            negativity_score = _match(
                flag,
                {
                    Flags.NEG_FLAIR_SENTIMENT: (
                        negativity_score - 0.2 * float(picked["pos"])
                    )
                    * 2,
                    Flags.NEG_MAP_SENTIMENT: negativity_score
                    - 0.2 * float(picked["neg"]),
                    Flags.POS_SENTIMENT: negativity_score - 0.2,
                    Flags.CONTAINS_LAUGHING_EMOJI: negativity_score - 0.2,
                    Flags.EMOJIS_ARE_POSITIVE: negativity_score - 0.2,
                    Flags.NEG_SENTIMENT: negativity_score + 0.5,
                    Flags.NEG_FLAIR_CONTRADICTING: negativity_score - 0.2,
                    Flags.NEG_FLAIR_CONJUGATIONS: negativity_score - 0.2,
                    Flags.POS_FLAIR_CONJUGATIONS: negativity_score + 0.2,
                },
            )

        rating = min(5, (round(1 - negativity_score, 4) / 2))
        return round(min(5, rating * 10)) if rounded else rating
