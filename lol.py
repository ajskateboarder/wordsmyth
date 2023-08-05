"""Wrappers over Flair and TorchMoji to simplify model prediction"""
from threading import Lock
from typing import Dict, Union

from flair.data import Sentence
from flair.splitter import SegtokSentenceSplitter
from flair.models import TextClassifier


class Flair:
    """Abstracted Flair `en-sentiment` sentiment classifier"""

    def __init__(self) -> None:
        self.sia = TextClassifier.load("en-sentiment")
        self.lock = Lock()

    def predict(self, text: str) -> Dict[str, Union[str, float]]:
        """Predict text sentiment in a thread-safe manner"""

        with self.lock:
            print(SegtokSentenceSplitter().split(text))
            sentence = Sentence(text)
            self.sia.predict(sentence)

            sent = sentence.labels[0]
            score = sentence.score

        return repr(sentence)


p = Flair().predict(
    "I'd love to write a review of this magazine.  But I can't if I don't have anything to read.  I was a subscriber since day 1, and then about a year ago or so, they just stopped coming.  I've tried everything, called, written, stood on my head, everything I can think of to get my issues delivered and nothing.  And noone at Hearst takes any responsibility.  It is ridiculous.  Run far away for this subscribtion."
)
print(p)
