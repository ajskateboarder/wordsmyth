import json

with open("./output.json", encoding="utf-8") as fh:
    data = json.load(fh)
print("sentiment,score,text")

for d in data:
    print(f"{d['sentiment']['sentiment']},{d['sentiment']['score']},\"{d['text']}\"")
