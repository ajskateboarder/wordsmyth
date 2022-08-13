import json

with open('data.json') as fh:
    data = json.load(fh)

print(data)