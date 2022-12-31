"""Statically analyze the compiled JSON and compile an HTML page with the results"""
import json
import numpy as np

with open("emojimap.json", encoding="utf-8") as fh:
    em = json.load(fh)

with open("data.json", encoding="utf-8") as fh:
    data = json.load(fh)

finals = []
elements = []

for elem in data:
    picked = [e for e in em if elem.get("fixed", elem["emoji"]) == e["repr"]][0]
    score = np.mean([float(picked["pos"]), float(picked["neu"]), float(picked["neg"])])
    em_mean = np.mean([float(e["score"]) for e in em if e["repr"] in elem["emojis"]])

    if elem["sentiment"]["flair"] == "neg":
        score = (score - 0.2 * float(picked["pos"])) * 2
    if elem["sentiment"]["map"] == "neg":
        score = score - 0.2 * float(picked["neg"])
    if elem["sentiment"]["map"] == "pos" and elem["sentiment"]["flair"] == "pos":
        score = score - 0.2
    if "🤣" in elem["content"]:
        score = score - 0.2
    if ":thumbsup:" in elem["emojis"]:
        score = score - 0.2
    if round(1 - score, 4) < 0.8667:
        score = score + abs(em_mean)

    finals.append(round(1 - score, 4))
    rating = round(1 - score, 4) / 2

    elements.append(
        # Panel(
        #     f"{elem['content']}\n{''.join(['★' for _ in range(round(rating * 10))]+['☆' for _ in range(5 - round(rating * 10))])} ({rating})\n{','.join(elem['emojis'])}",
        #     expand=True,
        # )
        f"<p>{elem['content']}<br>{''.join(['★' for _ in range(round(rating * 10))]+['☆' for _ in range(5 - round(rating * 10))])} ({rating})<br>{','.join(elem['emojis'])}</p>"
    )

final = np.mean(finals)
print("\n".join(elements))
