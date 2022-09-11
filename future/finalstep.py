import itertools

import pandas as pd

df = pd.read_csv("./extracts.csv")
texts = df[["text", "emojis", "sentiment"]]

vals = list(texts.to_dict().values())


def single_true(iterable):
    i = iter(iterable)
    return any(i) and not any(i)


for t, e, s in zip(vals[0].values(), vals[1].values(), vals[2].values()):
    emojis = e.split(", ")

    classes = [":confused:", ":thumbsup:", ":eyes:"]
    occurences = [e in emojis for e in classes]
    indices = [i for i, x in enumerate(occurences) if x is True]

    maps = list(emojis.index(classes[i]) for i in indices)

    if len(maps) == 2:
        print(t, "\n", f"{emojis[min(maps)]} at {min(maps)}", "\n", s.upper(), "\n")
