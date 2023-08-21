"""Wrappers over Flair and TorchMoji to simplify model prediction"""
from threading import Lock
from typing import Dict, Union

from flair.data import Sentence
from flair.models import TextClassifier


class Flair:
    """Abstracted Flair `en-sentiment` sentiment classifier"""

    def __init__(self) -> None:
        self.sia = TextClassifier.load("en-sentiment")
        self.lock = Lock()

    def predict(self, text: str) -> Dict[str, Union[str, float]]:
        """Predict text sentiment in a thread-safe manner"""

        with self.lock:
            sentence = Sentence(text)
            self.sia.predict(sentence)

            sent = sentence.labels[0]
            score = sentence.score

        if "POSITIVE" in str(sent):
            return {"sentiment": "pos", "score": score}
        if "NEGATIVE" in str(sent):
            return {"sentiment": "neg", "score": score}

        return {"sentiment": "neu", "score": score}
