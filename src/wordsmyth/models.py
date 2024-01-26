"""Wrappers over Flair and TorchMoji to simplify model prediction"""
from __future__ import annotations

import json
from threading import Lock

from flair.data import Sentence
from flair.models import TextClassifier
from torchmoji.model_def import torchmoji_emojis
from torchmoji.sentence_tokenizer import SentenceTokenizer
import numpy as np

from wordsmyth.constants import VOCAB_FILE_PATH, MODEL_WEIGHTS_PATH, EMOJIS


def top_elements(array: np.ndarray, k: int) -> np.ndarray:
    """Select maximum elements from Numpy array"""
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]


class TorchMoji:
    """Abstracted TorchMoji model"""

    def __init__(self) -> None:
        with open(VOCAB_FILE_PATH, encoding="utf-8") as fh:
            vocabulary = json.load(fh)

        max_sentence_length = 100
        self.tokenizer = SentenceTokenizer(vocabulary, max_sentence_length)
        self.model = torchmoji_emojis(MODEL_WEIGHTS_PATH, return_attention=True)

    def predict(self, text: str | list, top_n: int = 5) -> list[str]:
        """Emoji prediction"""

        if not isinstance(text, list):
            text = [text]

        probabilities, _ = self.model(self.tokenizer.tokenize_sentences(text)[0])

        emoji_ids = top_elements(probabilities[0], top_n)
        emojis = list(map(lambda x: EMOJIS[x], emoji_ids))

        return emojis

class Flair:
    """Abstracted Flair `en-sentiment` sentiment classifier"""

    def __init__(self) -> None:
        self.sia = TextClassifier.load("en-sentiment")
        self.lock = Lock()

    def predict(self, text: str) -> dict[str, str | float]:
        """Predict text sentiment"""

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
