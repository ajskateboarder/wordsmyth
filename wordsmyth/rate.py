from __future__ import annotations

import warnings
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Generator, Union

from .models.flair import Flair
from .models.torchmoji import TorchMoji

InputType = Union[str, "list[str]"]


def divide_list(l: list, n: int) -> Generator[list, None, None]:
    for i in range(0, len(l), n):
        yield l[i : i + n]


class Wordsmyth:
    def __init__(self) -> None:
        warnings.filterwarnings("ignore")
        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def model_eval(
        self, texts: list[str], emojis: int
    ) -> Generator[dict[str, Any], None, None]:
        """Evaluate multiple chunks of text through both Flair and TorchMoji"""
        texts = list(divide_list(texts, 5))
        with ThreadPoolExecutor(len(texts)) as pool:
            with ThreadPoolExecutor(len(texts)) as pool:
                flair = pool.map(self.flair, texts)
                torchmoji = pool.map(self.torchmoji, texts, repeat(emojis))
                for resf_, rest_, text_ in zip(flair, torchmoji, texts):
                    for resf, rest, text in zip(resf_, rest_, text_):
                        yield {"sentiment": resf, "emojis": rest, "text": text}

    def flair(self, text: InputType) -> list[dict[str, Union[str, float]]]:
        """Evaluate a single text or a list of texts through Flair's `en-sentiment` model"""
        if isinstance(text, str):
            text = [text]
        print(text)
        return [self._flair.predict(sentence) for sentence in text]

    def torchmoji(self, text: InputType, top_n: int) -> list[list[str]]:
        """Evaluate a single text or a list of texts through the TorchMoji model"""
        if isinstance(text, str):
            text = [text]
        return [self._torchmoji.predict(sentence, top_n=top_n) for sentence in text]
