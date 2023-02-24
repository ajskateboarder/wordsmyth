from __future__ import annotations
from typing import Union, Generator
from itertools import repeat
from pathos.multiprocessing import Pool

from .rate_utils import fix_content, rate

from .models.flair import Flair
from .models.torchmoji import TorchMoji

InputType = Union[str, list[str]]

class Wordsmyth:
    def __init__(self) -> None:
        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def model_eval(self, texts: list[list[str]], emojis: int) -> None:
        """Evaluate multiple chunks of text through both Flair and TorchMoji"""
        with Pool() as pool:
            for flair, torch in zip(pool.map(self.flair, texts), pool.map(self.torchmoji, texts, repeat(emojis))):
                pass

    def flair(self, text: InputType) -> Generator[dict[str, Union[str, float]], None, None]:
        """Evaluate a single text or a list of texts through Flair's `en-sentiment` model"""
        if isinstance(text, str):
            text = [text]
        return [self._flair.predict(sentence) for sentence in text]

    def torchmoji(
        self, text: InputType, top_n: int
    ) -> Generator[list[str], None, None]:
        """Evaluate a single text or a list of texts through the TorchMoji model"""
        if isinstance(text, str):
            text = [text]
        return [self._torchmoji.predict(sentence, top_n=top_n) for sentence in text]
