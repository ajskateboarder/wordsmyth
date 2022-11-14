import json
import numpy as np

with open("emojimap.json", encoding="utf-8") as fh:
    em = json.load(fh)

with open("data.json", encoding="utf-8") as fh:
    data = json.load(fh)


for elem in data:
    picked = [e for e in em if elem.get("fixed", elem["emoji"]) == e["repr"]][0]
    score = np.mean([float(picked["pos"]), float(picked["neu"]), float(picked["neg"])])

    if elem["sentiment"]["flair"] == "neg":
        score = (score - 0.2 * float(picked["pos"])) * 2
    if elem["sentiment"]["map"] == "neg":
        score = score - 0.2 * float(picked["neg"])
    if elem["sentiment"]["map"] == "pos" and elem["sentiment"]["flair"] == "pos":
        score = score - 0.2
    if "🤣" in elem["content"]:
        score = score - 0.2

    data[data.index(elem)]["rating"] = round(1 - score, 3)
    
with open("data.json", "w", encoding="utf-8") as fh:
    json.dump(data, fh)
