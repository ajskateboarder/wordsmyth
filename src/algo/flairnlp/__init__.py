"""
Simple docstring example
"""

from threading import Lock

from flair.models import TextClassifier
from flair.data import Sentence
from typing import Dict, Union

MUTEX = Lock()

class Flair:
    def __init__(self) -> None:
        self.sia = TextClassifier.load("en-sentiment")

    def predict(self, text: str) -> Dict[str, Union[str, float]]:
        MUTEX.acquire()
        try:
            sentence = Sentence(text)
            self.sia.predict(sentence)

            sent = sentence.labels[0]
            score = sentence.score
        finally:
            MUTEX.release()

        if "POSITIVE" in str(sent):
            return {"sentiment": "pos", "score": score}
        if "NEGATIVE" in str(sent):
            return {"sentiment": "neg", "score": score}
        
        return {"sentiment": "neu", "score": score}
