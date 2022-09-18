from pprint import pprint
import json
import pandas as pd

df = pd.read_csv("./extracts.csv")

with open('./emojimap.json', 'r', encoding='utf-8') as fh:
    em = json.load(fh)

em = {e["repr"]: e for e in em}
print(em)

texts = df[["text", "emojis", "sentiment"]]

vals = list(texts.to_dict().values())

def single_true(iterable):
    i = iter(iterable)
    return any(i) and not any(i)


objects = []
for t, e, s in zip(vals[0].values(), vals[1].values(), vals[2].values()):
    emojis = e.split(", ")

    classes = [":confused:", ":thumbsup:", ":eyes:"]
    occurences = [e in emojis for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    maps = list(emojis.index(classes[i]) for i in indices)

    if len(maps) == 2:
        reprr = emojis[min(maps)]
        match = em[reprr]
        
        obj = {
            "content": t,
            "emoji": reprr,
            "position": min(maps),
            "sentiment": {
                "flair": s,
                "map": match["sentiment"]
            },
            "emojis": emojis,
            "matches": s == match["sentiment"]
        }

        pprint(obj)
        objects.append(obj)
