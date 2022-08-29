import json
import itertools
import csv

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

with open("data.json") as fh:
    data = json.load(fh)

ab = list(itertools.chain(*[e for e in data]))

ratio = ["negative", "neutral", "positive"]

with open("data.csv", "w") as csv_file:
    fieldnames = [
        "text",
        "emoji",
        "sentiment",
        "neg",
        "neu",
        "pos",
        "compound",
        "detected",
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for emoji in ab:
        if not emoji["text"].startswith("\xa0@"):
            sentence = emoji["text"].strip()
            vs = analyzer.polarity_scores(sentence)
            sentiment = ratio[list(vs.values()).index(max(list(vs.values())[:-1]))]

            writer.writerow(
                {
                    "text": sentence,
                    "emoji": emoji["emoji"],
                    "sentiment": ratio[
                        list(vs.values()).index(max(list(vs.values())[:-1]))
                    ],
                    "neg": vs["neg"],
                    "neu": vs["neu"],
                    "pos": vs["pos"],
                    "detected": (True if sentiment != "neutral" else False),
                }
            )
