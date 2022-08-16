import json
import itertools

with open("data.json") as fh:
    data = json.load(fh)

ab = list(itertools.chain(*[e for e in data]))
