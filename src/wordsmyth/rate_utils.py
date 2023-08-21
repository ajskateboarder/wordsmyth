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
    """Assign a more accurate emoji to some text from TorchMoji output
    given Flair predictions and an emojimap.

    - `emojimap` is a mapping of emojis to their floating-point sentiment values in negativity,
        neutrality, and positivity
    - `text` is a combination of predictions from TorchMoji and Flair results

    https://kt.ijs.si/data/Emoji_sentiment_ranking/index.html"""
    # text uses data from this object to better adjust the results from TorchMoji to something more accurate.
    # emojimap is used to locate emojis which fit Flair's text predictions
    # as we have found this model to have a higher accuracy for detecting
    # base sentiment.

    # These emojis often show up in TorchMoji responses, so these are checked
    target_emojis = [":confused:", ":thumbsup:", ":eyes:", ":smile:", ":persevere:"]
    emoji_indices = find_indices(text.emojis, target_emojis)
    num_matches = len(emoji_indices)

    allowed_matches = [1, 2]
    leniency = False

    if num_matches not in allowed_matches:
        # If there were too many indexed emojis, add a lenience factor
        # This allows content to be rated but gets adjusted later on
        leniency = True
        allowed_matches.extend([3, 4])

    # Find the first emoji that matches one of the target emojis
    # Emojis closer to index 0 are often more accurate
    try:
        first_index = min(emoji_indices)
    except ValueError:
        return None
    first_emoji = text.emojis[first_index]
    match = emojimap[first_emoji]

    obj = {
        "content": text.text,
        "emoji": first_emoji,
        "position": first_index,
        "sentiment": {
            "flair": text.sentiment.sentiment,
            "map": match["sentiment"],
        },
        "emojis": text.emojis,
        "matches": text.sentiment.sentiment == match["sentiment"],
        "score": text.sentiment.score,
        "leniency": leniency,
    }

    # If the matched sentiment does not match the text sentiment, try to find a better match
    if obj["sentiment"]["flair"] != obj["sentiment"]["map"]:
        # Find emojis that match the text sentiment and are in the text emojis
        matching_emojis = [
            e
            for e in text.emojis
            if emojimap[e]["sentiment"] == text.sentiment.sentiment
            and emojimap[e]["repr"] in text.emojis
        ]

        # Find the index of the closest match
        sequence = [text.emojis.index(emojimap[e]["repr"]) for e in matching_emojis]
        closest_index = min(sequence) if sequence else None
        fixed = (
            emojimap.get(text.emojis[closest_index], {})
            if closest_index is not None
            else {}
        )

        # If the closest match has the same sentiment as the text, use it as the fixed emoji
        if text.sentiment == fixed.get("sentiment"):
            obj["fixed"] = fixed.get("repr")
            return {**obj, "status": "fixed"}

        emojis = [emojimap[emoji] for emoji in text.emojis]
        if [e["sentiment"] == "pos" for e in emojis].count(True) > [
            e["sentiment"] == "neg" for e in emojis
        ].count(True):
            obj["sentiment"]["map"] = "pos"
        else:
            obj["sentiment"]["map"] = "neg"

        target_emojis.remove(obj["emoji"])
        try:
            obj["emoji"] = emojimap[
                [
                    e
                    for e in text.emojis
                    if emojimap[e]["sentiment"] == obj["sentiment"]["flair"]
                ][0]
            ]["repr"]
        except IndexError:
            return {**obj, "status": "incorrect"}

        return {**obj, "status": "fixed"}

    return {**obj, "status": "correct"}


def rate(text: dict[str, Any], emojimap: list) -> Union[int, float]:
    """Rate"""

    emoji_repr = text.get("fixed") or text.get("emoji") or text["emojis"][0]
    picked_emojis = [e for e in emojimap if e["repr"] == emoji_repr]
    low_score = False

    picked = picked_emojis[0]
    score = np.mean([float(picked["pos"]), float(picked["neu"]), float(picked["neg"])])

    emojis_are_positive = [
        e["repr"] in text["emojis"]
        for e in [e for e in emojimap if e["sentiment"] == "pos"]
    ]
    emojis_are_negative = [
        e["repr"] in text["emojis"]
        for e in [e for e in emojimap if e["sentiment"] == "neg"]
    ]
    conjunctions = ["but", "although", "however"]

    if text["sentiment"]["flair"] == "neg":
        score = (score - 0.2 * float(picked["pos"])) * 2
    if text["sentiment"]["map"] == "neg":
        score = score - 0.2 * float(picked["neg"])
    if text["sentiment"]["map"] == "pos" and text["sentiment"]["flair"] == "pos":
        score = score - 0.2
    if "🤣" in text["content"]:
        score = score - 0.2
    if any(emojis_are_positive):
        score = score - 0.2
    if text["sentiment"]["map"] == "neg" and text["sentiment"]["flair"] == "neg":
        score = score + 0.5
    # Rules to check for contradicting outputs
    if text["score"] < 0.8 and emojis_are_negative.count(
        True
    ) < emojis_are_positive.count(True):
        low_score = True
        if text["sentiment"]["flair"] == "neg":
            score = score - 0.2
        if text["sentiment"]["map"] == "neg":
            score = score - 0.2
    if (
        any(word in text["content"].lower().strip() for word in conjunctions)
        and not low_score
    ):
        if text["sentiment"]["flair"] == "neg":
            score = score - 0.2
        if text["sentiment"]["flair"] == "pos":
            score = score + 0.2

    rating = min(5, (round(1 - score, 4) / 2))  # type: ignore
    return rating  # type: ignore
