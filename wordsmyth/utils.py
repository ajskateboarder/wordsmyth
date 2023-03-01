"""Post-processing utilities for algorithm data.

There's lots of strangely written logic and I don't expect anyone to understand how it works"""
from __future__ import annotations

from typing import Any
from typing import Union

import numpy as np


def find_indices(content: list[str], classes: list[str]) -> list[int]:
    """Find all indices of a list using another list"""
    occurences = [e in content for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    return [content.index(classes[i]) for i in indices]


def fix_content(text: dict, emojimap: dict) -> Union[dict[str, Any], None]:
    """Assign a more accurate emoji to a text given TorchMoji and Flair output"""

    # These emojis often show up in TorchMoji responses, so these are checked
    emojis = text["emojis"]
    target_emojis = [":confused:", ":thumbsup:", ":eyes:", ":smile:"]
    emoji_indices = find_indices(emojis, target_emojis)
    num_matches = len(emoji_indices)

    if num_matches in (1, 2):
        # Find the first emoji that matches one of the target emojis
        first_index = min(emoji_indices)
        first_emoji = emojis[first_index]
        match = emojimap[first_emoji]

        # Build the output object
        obj = {
            "content": text["text"],
            "emoji": first_emoji,
            "position": first_index,
            "sentiment": {"flair": text["sentiment"]["sentiment"], "map": match["sentiment"]},
            "emojis": emojis,
            "matches": text["sentiment"]["sentiment"] == match["sentiment"],
            "score": text["sentiment"]["score"],
        }

        # If the matched sentiment does not match the text sentiment, try to find a better match
        if obj["sentiment"]["flair"] != obj["sentiment"]["map"]:
            # Find emojis that match the text sentiment and are in the text emojis
            matching_emojis = [
                e for e in emojis
                if emojimap[e]["sentiment"] == text["sentiment"]
                and emojimap[e]["repr"] in emojis
            ]

            # Find the index of the closest match
            sequence = [emojis.index(emojimap[e]["repr"]) for e in matching_emojis]
            closest_index = min(sequence) if sequence else None
            fixed = emojimap.get(emojis[closest_index], {}) if closest_index is not None else {}

            # If the closest match has the same sentiment as the text, use it as the fixed emoji
            if text["sentiment"] == fixed.get("sentiment"):
                obj["fixed"] = fixed.get("repr")
                return {**obj, "status": "fixed"}

            return {**obj, "status": "incorrect"}

        return {**obj, "status": "correct"}

    return None


def rate(text: dict[str, Any], emojimap: list) -> Union[int, float]:
    positive_emojis = [e for e in emojimap if e["sentiment"] == "pos"]
    emoji_repr = text.get("fixed") or text.get("emoji")
    picked_emojis = [e for e in emojimap if e["repr"] == emoji_repr]

    picked = picked_emojis[0]
    score = np.mean([float(picked["pos"]), float(picked["neu"]), float(picked["neg"])])
    em_mean = np.mean([float(e["score"]) for e in emojimap if e["repr"] in text["emojis"]])

    if text["sentiment"]["flair"] == "neg":
        score = (score - 0.2 * float(picked["pos"])) * 2
    if text["sentiment"]["map"] == "neg":
        score = score - 0.2 * float(picked["neg"])
    if text["sentiment"]["map"] == "pos" and text["sentiment"]["flair"] == "pos":
        score = score - 0.2
    if "🤣" in text["content"]:
        score = score - 0.2
    if any(e["repr"] in text["emojis"] for e in positive_emojis):
        score = score - 0.2
    if text["sentiment"]["map"] == "neg" and text["sentiment"]["flair"] == "neg":
        score = score + 0.5
    if round(1 - score, 4) < 0.8667:
        score = score - abs(em_mean)

    rating = min(5, (round(1 - score, 4) / 2))  # type: ignore
    return rating  # type: ignore
