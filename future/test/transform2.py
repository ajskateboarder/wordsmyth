import json
from algorithms.wrapper import dump_csv

with open("stream.json", encoding="utf-8") as fh:
    thing = dump_csv(json.load(fh))
print(thing)