import json
import itertools
from emoji import emojize

with open("data.json") as fh:
    data = json.load(fh)

with open("esranks.json") as fh:
    emojis: "list[dict]" = json.load(fh)
    classes = [e["emoji_repr"] for e in emojis]

ab = list(itertools.chain(*[e for e in data]))

for emoji in ab:
    if not emoji["text"].startswith("\xa0@"):
        print(emoji["text"].strip(), emoji["emoji"], "\n")
        print(emojis[classes.index(emoji["emoji"])])
