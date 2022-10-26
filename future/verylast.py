import json
import numpy as np

with open("emojimap.json", encoding="utf-8") as fh:
    em = json.load(fh)

with open("data.json", encoding="utf-8") as fh:
    data = json.load(fh)

# elem = data[-4]

for elem in data:
    print(elem["content"])
    picked = [e for e in em if elem["emoji"] == e["repr"]][0]
    score = np.mean([float(picked["pos"]), float(picked["neu"]), float(picked["neg"])])
    print(elem["sentiment"])

    if elem["sentiment"]["flair"] == "neg":
        score = (score - 0.2 * float(picked["pos"])) * 2
    if elem["sentiment"]["map"] == "neg":
        score = score - 0.2 * float(picked["neg"])

    print(round(1 - score, 3), "\n")
