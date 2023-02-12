"""Post-processing utilities for algorithm data"""
import numpy as np


def find_indices(content, classes):
    occurences = [e in content for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    return list(content.index(classes[i]) for i in indices)


def mse(actual, predicted):
    return np.square(np.subtract(np.array(actual), np.array(predicted))).mean()


def fix_content(text: dict, emojimap: dict):
    emojis = text["emojis"]

    maps = find_indices(emojis, [":confused:", ":thumbsup:", ":eyes:"])

    if len(maps) == 2 or len(maps) == 1:
        reprr = emojis[min(maps)]
        match = emojimap[reprr]

        obj = {
            "content": text["text"],
            "emoji": reprr,
            "position": min(maps),
            "sentiment": {"flair": text["sentiment"], "map": match["sentiment"]},
            "emojis": emojis,
            "matches": text["sentiment"] == match["sentiment"],
            "score": text["score"],
        }

        if obj["sentiment"]["flair"] != obj["sentiment"]["map"]:
            sequence = list(
                obj["emojis"].index(emojimap[e]["repr"])
                for e in emojis
                if emojimap[e]["sentiment"] == text["sentiment"]
                and emojimap[e]["repr"] in obj["emojis"]
            )

            newst = emojimap.get(
                (obj["emojis"][min(sequence)] if len(sequence) > 0 else ""), {}
            )

            if text["sentiment"] == newst.get("sentiment"):
                obj["fixed"] = newst.get("repr")
                obj["status"] = "fixed"
                return obj
            obj["status"] = "incorrect"
            return obj
        obj["status"] = "correct"
        return obj


def rate(text: dict, emojimap: list):
    positive_emojis = [e for e in emojimap if e["sentiment"] == "pos"]

    picked = [e for e in emojimap if text.get("fixed", text["emoji"]) == e["repr"]][0]
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

    rating = round(1 - score, 4) / 2
    return rating
