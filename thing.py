import json
import itertools

with open("data.json") as fh:
    data = json.load(fh)

ab = list(itertools.chain(*[e for e in data]))

for emoji in ab:
    if not emoji["text"].startswith("\xa0@"):
        print(emoji["text"].strip(), emoji["emoji"], "\n")
