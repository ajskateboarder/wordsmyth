import pandas as pd

# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from algo.roberta import Roberta
from flair.models import TextClassifier
from flair.data import Sentence


df = pd.read_csv("./data.csv")
sia = TextClassifier.load("en-sentiment")


def flair_prediction(x):
    sentence = Sentence(x)
    sia.predict(sentence)
    sent = sentence.labels[0]
    score = sentence.score

    if "POSITIVE" in str(sent):
        return f"pos {score}"
    elif "NEGATIVE" in str(sent):
        return f"neg {score}"
    else:
        return f"neu {score}"


df["flair_sent"] = df["text"].apply(flair_prediction)
df.to_csv("./data.csv")
