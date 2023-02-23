import json
import logging
import pickle
import warnings
from io import StringIO

import luigi
import pandas as pd
from luigi.format import Nop
from luigi.util import requires

from wordsmyth import Wordsmyth
from wordsmyth.pipeline.plot import catplot_comments
from wordsmyth.rate import fix_content, rate

warnings.filterwarnings("ignore")

logging.basicConfig(filename="data/pipeline.log")
logger = logging.getLogger()

with open("emojimap.json", encoding="utf-8") as fh:
    em = {e["repr"]: e for e in json.load(fh)}
    # em[":cry:"]["sentiment"] = "neg"
    # em[":grimacing:"]["sentiment"] = "neu"
    pem = json.load(fh)


class CommentSource(luigi.Task):
    comments = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.comments)


@requires(CommentSource)
class ModelEval(luigi.Task):
    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget("data/comments.pkl", format=Nop)

    def run(self) -> None:
        with self.input().open("r") as infile:
            comments = (
                pd.read_json(StringIO(infile.read()))[["reviewText", "overall"]]
                .head(300)
                .drop_duplicates(["reviewText"])
                .reset_index(drop=True)
            )

        outputs = []

        for flair, torch, actual_rating in zip(
            predict_flair(comments.reviewText),
            predict_torchmoji(comments.reviewText, emojis=10),
            comments["overall"],
        ):
            print(flair, torch)
            comment = dict(torch, **flair)
            df = pd.json_normalize(comment).assign(**comment["sentiment"])

            text = df[["text", "emojis", "sentiment", "score"]]
            fixed = fix_content(text.to_dict("records")[0], em)

            if fixed is not None:
                text["flair"] = df["sentiment.sentiment"]
                text["map"] = fixed.sentiment.map
                text["overall"] = actual_rating
                text["fixed"] = fixed
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
            itemdict = {key: getattr(item, key) for key in dir(item) if not "_" in key}
            fixed = {
                k: v
                for k, v in itemdict.items()
                if not k in ("count", "Index", "index")
            }["fixed"]
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
