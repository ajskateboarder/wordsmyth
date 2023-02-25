import json
import logging
import pickle
import warnings
from io import StringIO

import luigi
import pandas as pd
import numpy as np
from luigi.format import Nop
from luigi.util import requires

from wordsmyth import Wordsmyth
from wordsmyth.utils import fix_content, rate
from wordsmyth.pipeline.plot import catplot_comments

warnings.filterwarnings("ignore")

logging.basicConfig(filename="data/pipeline.log")
logger = logging.getLogger()

with open("emojimap.json", encoding="utf-8") as fh:
    pem = json.load(fh)
    em = {e["repr"]: e for e in pem}
    # These sentiments were objectively incorrect so they are adjusted
    em[":cry:"]["sentiment"] = "neg"
    em[":grimacing:"]["sentiment"] = "neu"


class CommentSource(luigi.Task):
    comments = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.comments)


@requires(CommentSource)
class ModelEval(luigi.Task):
    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget("data/comments.pkl", format=Nop)

    def run(self) -> None:
        ws = Wordsmyth()

        with self.input().open("r") as infile:
            comments = (
                pd.read_json(StringIO(infile.read()))[["reviewText", "overall"]]
                .head(300)
                .drop_duplicates(["reviewText"])
                .reset_index(drop=True)
            )

        outputs = []
        review_texts = [e.replace("\n", "") for e in comments["reviewText"].to_list()]

        for comment, actual_rating in zip(
            ws.model_eval(review_texts, emojis=10),
            comments["overall"],
        ):
            df = pd.json_normalize(comment).assign(**comment["sentiment"])

            text = df[["text", "emojis", "sentiment", "score"]]
            fixed = fix_content(text.to_dict("records")[0], em)

            if fixed is not None:
                text["flair"] = df["sentiment.sentiment"]
                text["map"] = fixed["sentiment"]["map"]
                text["overall"] = actual_rating
                text["fixed"] = json.dumps(fixed)
                outputs.append(text)

        with self.output().open("wb") as outfile:
            pickle.dump(pd.concat(outputs), outfile)


@requires(ModelEval)
class Rate(luigi.Task):
    def output(self):
        return luigi.LocalTarget("data/reviews.pkl", format=Nop)

    def run(self):
        with self.input().open("rb") as infile:
            data: pd.DataFrame = pickle.load(infile)
        ratings = []
        for item in data.itertuples():
            # NOTE: This can most likely be replaced by a dot-access method
            fixed = json.loads(item[-1])
            ratings.append(round(rate(fixed, pem) * 10, 4))
        data["rating"] = ratings
        with self.output().open("wb") as outfile:
            pickle.dump(data, outfile)


@requires(Rate)
class RateTable(luigi.Task):
    def run(self):
        with self.input().open("rb") as infile:
            data: pd.DataFrame = pickle.load(infile)
        data = data.drop_duplicates(["text"]).reset_index(drop=True)

        print(data[["overall", "rating", "text", "score"]])
        print(data.describe())
        print(data["rating"].mean())


@requires(Rate)
class RatePlot(luigi.Task):
    output_path = luigi.Parameter(default="data/output.png")
    dark = luigi.BoolParameter()

    def run(self):
        with self.input().open("rb") as infile:
            data: pd.DataFrame = pickle.load(infile)

        plot = catplot_comments(data, self.dark)
        plot.savefig(self.output_path)


if __name__ == "__main__":
    luigi.run()
