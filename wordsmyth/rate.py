from __future__ import annotations
from typing import Union, Generator
from itertools import repeat
from multiprocessing import Pool

from .utils import fix_content, rate

from .models.flair import Flair
from .models.torchmoji import TorchMoji

InputType = Union[str, "list[str]"]


class Wordsmyth:
    def __init__(self) -> None:
        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def _flaircb(self, texts):
        out = []
        for text in self.flair(texts):
            out.append(text)
        return out

    def _torchmojicb(self, texts, emojis):
        return list(list(self.torchmoji(text, emojis)) for text in texts)

    def model_eval(self, texts: list[list[str]], emojis: int):
        """Evaluate multiple chunks of text through both Flair and TorchMoji"""
        print("AAAA")
        pool = Pool(5)
        print(pool.map(self._flaircb, texts))

    def flair(
        self, text: InputType
    ) -> Generator[dict[str, Union[str, float]], None, None]:
        """Evaluate a single text or a list of texts through Flair's `en-sentiment` model"""
        if isinstance(text, str):
            text = [text]
        for sentence in text:
            yield self._flair.predict(sentence)

    def torchmoji(
        self, text: InputType, top_n: int
    ) -> Generator[list[str], None, None]:
        """Evaluate a single text or a list of texts through the TorchMoji model"""
        if isinstance(text, str):
            text = [text]
        for sentence in text:
            yield self._torchmoji.predict(sentence, top_n=top_n)
