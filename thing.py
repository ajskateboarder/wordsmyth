import json

with open("data.json") as fh:
    data = json.load(fh)

d: "list[str, str]"
for d in data:
    if not d[1].startswith("'\\xa0@") or not d[1].startswith('"'):
        print(d[1])
