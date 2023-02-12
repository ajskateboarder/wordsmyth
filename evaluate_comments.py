import warnings
warnings.filterwarnings("ignore")

import json

from pandas import json_normalize
import luigi

from algorithms import predict_flair, predict_torchmoji
from utils import fix_content, rate

with open("emojimap.json", encoding="utf-8") as fh:
    em = {e["repr"]: e for e in json.load(fh)}
    em[":cry:"]["sentiment"] = "neg"
    em[":grimacing:"]["sentiment"] = "neu"

with open("emojimap.json", encoding="utf-8") as fh:
    rateem = json.load(fh)

class PrintComments(luigi.Task):
    def requires(self):
        class _GetComments(luigi.Task):
            def output(self):
                return luigi.LocalTarget("comments.json")

        return _GetComments()

    def run(self):
        with self.input().open("r") as infile:
            comments = json.load(infile)
        for flair, torch in zip(predict_flair(comments), predict_torchmoji(comments, emojis=10)):
            comment = dict(torch, **flair)
            df = json_normalize(comment).assign(**comment["sentiment"])
            text = df[["text", "emojis", "sentiment", "score"]].to_dict("records")[0]
            fixed = fix_content(text, em)
            if fixed is not None:
                print(
                    "[*]",
                    round(rate(fixed, rateem), 3) * 10,
                    text["text"],
                    text["emojis"],
                    "\n",
                )


if __name__ == "__main__":
    luigi.run()
