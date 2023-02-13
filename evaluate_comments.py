from wordsmyth.post import fix_content, rate
from wordsmyth.models import predict_flair, predict_torchmoji
import luigi
from luigi.format import Nop
from luigi.util import requires
import plotly.express as px
import pandas as pd
import pickle
from io import StringIO
import json
import warnings
import logging

warnings.filterwarnings("ignore")


logging.basicConfig(filename="pipeline.log")
logger = logging.getLogger()

with open("emojimap.json", encoding="utf-8") as fh:
    em = {e["repr"]: e for e in json.load(fh)}
    em[":cry:"]["sentiment"] = "neg"
    em[":grimacing:"]["sentiment"] = "neu"

with open("emojimap.json", encoding="utf-8") as fh:
    rateem = json.load(fh)


class CommentSource(luigi.Task):
    comments = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.comments)


@requires(CommentSource)
class ModelEval(luigi.Task):
    def output(self):
        return luigi.LocalTarget("comments.pkl", format=Nop)

    def run(self):
        with self.input().open("r") as infile:
            comments = pd.read_json(StringIO(infile.read()))[
                ["reviewText", "overall"]
            ].head(50)
        outputs = []

        for flair, torch, actual_rating in zip(
            predict_flair(comments.reviewText),
            predict_torchmoji(comments.reviewText, emojis=10),
            comments["overall"],
        ):
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
        return luigi.LocalTarget("reviews.pkl", format=Nop)

    def run(self):
        with self.input().open("rb") as infile:
            data: pd.DataFrame = pickle.load(infile)
        ratings = []
        for item in data.itertuples():
            # NOTE: This can most likely be replaced by a dot-access method
            itemdict = {key: getattr(item, key) for key in item.__match_args__}
            fixed = {k: v for k, v in itemdict.items() if not k in ("count", "Index", "index")}["fixed"]
            ratings.append(round(rate(fixed, rateem) * 10, 4))
        data["rating"] = ratings
        with self.output().open("wb") as outfile:
            pickle.dump(data, outfile)

@requires(Rate)
class RateTable(luigi.Task):
    def run(self):
        with self.input().open("rb") as infile:
            data: pd.DataFrame = pickle.load(infile)
        
        print(data[["overall", "rating", "text"]])

@requires(Rate)
class RatePlot(luigi.Task):
    output_path = luigi.Parameter(default="output.html")

    def run(self):
        with self.input().open("rb") as infile:
            data: pd.DataFrame = pickle.load(infile)

        data = data.loc[data.astype(str).drop_duplicates().index]

        fig = px.scatter(
            data, x='overall', y='rating', opacity=0.65,
            trendline='ols', trendline_color_override='darkblue'
        )
        fig.write_html(self.output_path)


if __name__ == "__main__":
    luigi.run()
