import warnings
warnings.filterwarnings("ignore")

import json

from pandas import json_normalize
from luigi.utils import requires
import luigi

from wordsmyth.models import predict_flair, predict_torchmoji
from wordsmyth.post import fix_content, rate

with open("emojimap.json", encoding="utf-8") as fh:
    em = {e["repr"]: e for e in json.load(fh)}
    em[":cry:"]["sentiment"] = "neg"
    em[":grimacing:"]["sentiment"] = "neu"

with open("emojimap.json", encoding="utf-8") as fh:
    rateem = json.load(fh)

class CommentSource(luigi.Task):
    comments = luigi.Parameter(default="comments.json")

    def output(self):
        return luigi.LocalTarget(self.comments)


@requires(CommentSource)
class RateComments(luigi.Task):
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
