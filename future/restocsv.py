import csv
import json

with open("output.json", encoding="utf-8") as fh:
    data = json.load(fh)

with open("data.csv", "w", encoding="utf-8") as fh:
    fields = ["sentiment", "score", "text"]
    writer = csv.DictWriter(fh, fields)

    writer.writeheader()
    for d in data:
        writer.writerow(
            {
                "sentiment": d["sentiment"]["sentiment"],
                "score": d["sentiment"]["score"],
                "text": d["text"],
            }
        )
