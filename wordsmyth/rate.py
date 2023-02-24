from __future__ import annotations
import warnings
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Generator, Union

from .rate_utils import fix_content, rate

from .models.flair import Flair
from .models.torchmoji import TorchMoji

InputType = Union[str, list[str]]

class Wordsmyth:
    def __init__(self) -> None:
        warnings.filterwarnings("ignore")
        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def model_eval(self, texts: list[list[str]], emojis: int) -> Generator[dict[str, Any], None, None]:
        """Evaluate multiple chunks of text through both Flair and TorchMoji"""
        with ThreadPoolExecutor(len(texts)) as pool:
            with ThreadPoolExecutor(len(texts)) as pool:
                flair = pool.map(self.flair, texts)
                torchmoji = pool.map(self.torchmoji, texts, repeat(emojis))
                for resf_, rest_, text_ in zip(flair, torchmoji, texts):
                    for resf, rest, text in zip(resf_, rest_, text_):
                        yield {**resf, "emojis": rest, "text": text}

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
