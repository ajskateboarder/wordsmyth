"""Post-processing utilities for algorithm data"""
from __future__ import annotations

from typing import Union

import numpy as np

from .types import Item


def find_indices(content: list[str], classes: list[str]) -> list[int]:
    """Helper function to find all indices of a list using another list"""
    occurences = [e in content for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    return list(content.index(classes[i]) for i in indices)


def fix_content(text: dict, emojimap: dict) -> Union[Item, None]:
    """Assign a more accurate emoji to a text given TorchMoji and Flair output"""

    # These emojis often show up in TorchMoji responses, so these are checked
    emojis = text["emojis"]
    maps = find_indices(emojis, [":confused:", ":thumbsup:", ":eyes:"])

    if len(maps) == 2 or len(maps) == 1:
        # Emojis closer to the front are often more accurate
        first = emojis[min(maps)]
        match = emojimap[first]

        obj = {
            "content": text["text"],
            "emoji": first,
            "position": min(maps),
            "sentiment": {"flair": text["sentiment"], "map": match["sentiment"]},
            "emojis": emojis,
            "matches": text["sentiment"] == match["sentiment"],
            "score": text["score"],
        }

        if obj["sentiment"]["flair"] != obj["sentiment"]["map"]:
            # Find emojis that match the text sentiment and in text emojis
            # then pick the emoji closest to the front
            sequence = [
                obj["emojis"].index(emojimap[e]["repr"])
                for e in emojis
                if emojimap[e]["sentiment"] == text["sentiment"]
                and emojimap[e]["repr"] in obj["emojis"]
            ]

            fixed = emojimap.get(
                (obj["emojis"][min(sequence)] if len(sequence) > 0 else ""), {}
            )

            if text["sentiment"] == fixed.get("sentiment"):
                obj["fixed"] = fixed.get("repr")
                obj["status"] = "fixed"
                return Item(**obj)

            obj["status"] = "incorrect"
            return Item(**obj)

        obj["status"] = "correct"
        return Item(**obj)
    return None


def rate(text: Item, emojimap: list) -> Union[int, float]:
    positive_emojis = [e for e in emojimap if e["sentiment"] == "pos"]

    picked = [e for e in emojimap if (text.fixed or text.emoji) == e["repr"]][0]
    score = np.mean([float(picked["pos"]), float(picked["neu"]), float(picked["neg"])])
    em_mean = np.mean([float(e["score"]) for e in emojimap if e["repr"] in text.emojis])

    if text.sentiment.flair == "neg":
        score = (score - 0.2 * float(picked["pos"])) * 2
    if text.sentiment.map == "neg":
        score = score - 0.2 * float(picked["neg"])
    if text.sentiment.map == "pos" and text.sentiment.flair == "pos":
        score = score - 0.2
    if "🤣" in text.content:
        score = score - 0.2
    if any(e["repr"] in text.emojis for e in positive_emojis):
        score = score - 0.2
    if text.sentiment.map == "neg" and text.sentiment.flair == "neg":
        score = score + 0.5
    if round(1 - score, 4) < 0.8667:
        score = score - abs(em_mean)

    rating = min(5, (round(1 - score, 4) / 2))  # type: ignore
    return rating  # type: ignore
