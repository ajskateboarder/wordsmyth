"""Post-processing utilities for algorithm data.

There's lots of strangely written logic and I don't expect anyone to understand how it works"""
from __future__ import annotations

from typing import Any, Optional, Union
import numpy as np
import wordsmyth.items


def find_indices(content: list[str], classes: list[str]) -> list[int]:
    """Find all indices of a list using another list"""
    occurences = [e in content for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    return [content.index(classes[i]) for i in indices]


def fix_content(
    text: wordsmyth.items.Output, emojimap: dict
) -> Optional[dict[str, Any]]:
    """Assign a more accurate emoji to some text from TorchMoji output given Flair predictions.

    `text` is a combination of predictions from TorchMoji and Flair results. This function uses
    data from this object to better adjust the results from TorchMoji to something more accurate.

    `emojimap` is a mapping of emojis to their floating-point sentiment values in negativity,
    neutrality, and positivity. We use this additional information to locate emojis which fit
    Flair's text predictions, as we have found this model to have a higher accuracy for detecting
    base sentiment.

    The mentioned data is from [here](https://kt.ijs.si/data/Emoji_sentiment_ranking/index.html)
    """

    # These emojis often show up in TorchMoji responses, so these are checked
    emojis = text["emojis"]
    target_emojis = [":confused:", ":thumbsup:", ":eyes:", ":smile:"]
    emoji_indices = find_indices(emojis, target_emojis)
    num_matches = len(emoji_indices)

    if num_matches in (1, 2):
        # Find the first emoji that matches one of the target emojis
        # Emojis closer to index 0 are often more accurate
        first_index = min(emoji_indices)
        first_emoji = emojis[first_index]
        match = emojimap[first_emoji]

        # Build the output object
        obj = {
            "content": text["text"],
            "emoji": first_emoji,
            "position": first_index,
            "sentiment": {
                "flair": text["sentiment"]["sentiment"],
                "map": match["sentiment"],
            },
            "emojis": emojis,
            "matches": text["sentiment"]["sentiment"] == match["sentiment"],
            "score": text["sentiment"]["score"],
        }

        # If the matched sentiment does not match the text sentiment, try to find a better match
        if obj["sentiment"]["flair"] != obj["sentiment"]["map"]:
            # Find emojis that match the text sentiment and are in the text emojis
            matching_emojis = [
                e
                for e in emojis
                if emojimap[e]["sentiment"] == text["sentiment"]
                and emojimap[e]["repr"] in emojis
            ]

            # Find the index of the closest match
            sequence = [emojis.index(emojimap[e]["repr"]) for e in matching_emojis]
            closest_index = min(sequence) if sequence else None
            fixed = (
                emojimap.get(emojis[closest_index], {})
                if closest_index is not None
                else {}
            )

            # If the closest match has the same sentiment as the text, use it as the fixed emoji
            if text["sentiment"] == fixed.get("sentiment"):
                obj["fixed"] = fixed.get("repr")
                return {**obj, "status": "fixed"}

            return {**obj, "status": "incorrect"}

        return {**obj, "status": "correct"}

    return None


def rate(text: dict[str, Any], emojimap: list) -> Union[int, float]:
    """Rate"""

    positive_emojis = [e for e in emojimap if e["sentiment"] == "pos"]
    emoji_repr = text.get("fixed") or text.get("emoji") or text["emojis"][0]
    picked_emojis = [e for e in emojimap if e["repr"] == emoji_repr]

    picked = picked_emojis[0]
    score = np.mean([float(picked["pos"]), float(picked["neu"]), float(picked["neg"])])
    em_mean = np.mean(
        [float(e["score"]) for e in emojimap if e["repr"] in text["emojis"]]
    )

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
