"""Wrappers over Flair and TorchMoji to simplify model prediction"""
from threading import Lock
from typing import Dict
from typing import Union

from flair.data import Sentence
from flair.models import TextClassifier

LOCK = Lock()


class Flair:
    def __init__(self) -> None:
        self.sia = TextClassifier.load("en-sentiment")

    def predict(self, text: str) -> Dict[str, Union[str, float]]:
        """Sentiment prediction with some mutex stuff"""

        with LOCK:
            sentence = Sentence(text)
            self.sia.predict(sentence)

            sent = sentence.labels[0]
            score = sentence.score

        if "POSITIVE" in str(sent):
            return {"sentiment": "pos", "score": score}
        if "NEGATIVE" in str(sent):
            return {"sentiment": "neg", "score": score}

        return {"sentiment": "neu", "score": score}
