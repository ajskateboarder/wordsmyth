"""Statically analyze the compiled JSON and generate a rating as a decimal"""
import json
import numpy as np

from rich.panel import Panel
from rich.console import Console
from rich.columns import Columns

with open("emojimap.json", encoding="utf-8") as fh:
    em = json.load(fh)

with open("data.json", encoding="utf-8") as fh:
    data = json.load(fh)
finals = []


def mse(actual, predicted):
    return np.square(np.subtract(np.array(actual), np.array(predicted))).mean()


renderables = []
negative_emojis = [e["repr"] for e in em if e["sentiment"] == "neg"]
positive_emojis = [e["repr"] for e in em if e["sentiment"] == "pos"]

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
    if any(emoji in negative_emojis for emoji in elem["emojis"]):
        score = score + 0.2
    if len([emoji for emoji in elem["emojis"] if emoji in positive_emojis]) > 2:
        score = score - 0.2
    if round(1 - score, 4) < 0.8667:
        score = score + abs(em_mean)

    finals.append(round(1 - score, 4))
    rating = round(1 - score, 4) / 2
    error = mse(elem["overall"], rating * 2)

    renderables.append(
        Panel(
            f"{elem['content']}\n{''.join(['★' for _ in range(round(rating * 10))]+['☆' for _ in range(5 - round(rating * 10))])} ({rating}) {error} {elem['overall']}\n{','.join(elem['emojis'])}",
            expand=True,
        )
    )

console = Console()
console.print(Columns(renderables))

print(np.mean(finals))
