from __future__ import annotations

import json
import warnings
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from typing import Generator, Union

import attrs

from .constants import DIR_PATH
from .models.flair import Flair
from .models.torchmoji import TorchMoji
from .rate_utils import fix_content, rate

InputType = Union[str, "list[str]"]


def divide_list(l: list, n: int) -> Generator[list, None, None]:
    for i in range(0, len(l), n):
        yield l[i : i + n]


@attrs.define
class Sentiment:
    sentiment: str
    score: float


@attrs.define
class Output:
    sentiment: Sentiment
    emojis: list[str]
    text: str

    def rating(self):
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            rate_map = json.load(emojimap)
        fixed = self._fix_content()
        return rate(fixed, rate_map)

    def _fix_content(self):
        with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
            fix_map = {e["repr"]: e for e in json.load(emojimap)}
            fix_map[":cry:"]["sentiment"] = "neg"
            fix_map[":grimacing:"]["sentiment"] = "neu"
        return fix_content(attrs.asdict(self), fix_map)


class Pipeline:
    def __init__(self) -> None:
        warnings.filterwarnings("ignore")
        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def eval(
        self, text: Union[list[str], str], emojis: int
    ) -> Union[Generator[Output, None, None], Output]:
        """Evaluate a text/list of text through both Flair and TorchMoji"""
        if isinstance(text, str):
            torchmoji = self._torchmoji.predict(text)
            flair = self._flair.predict(text)
            return Output(
                sentiment=Sentiment(**flair),
                emojis=torchmoji,
                text=text
            )

        text = list(divide_list(text, 5))
        with ThreadPoolExecutor(len(text)) as pool:
            flair = pool.map(self.flair, text)
            torchmoji = pool.map(self.torchmoji, text, repeat(emojis))
            for resf_, rest_, text_ in zip(flair, torchmoji, text):
                return (
                    Output(sentiment=Sentiment(**fl_result), emojis=tm_result, text=input_text)
                    for fl_result, tm_result, input_text in zip(resf_, rest_, text_)
                )

    def flair(self, text: InputType) -> list[dict[str, Union[str, float]]]:
        """Evaluate a single text or a list of texts through Flair's `en-sentiment` model"""
        if isinstance(text, str):
            text = [text]
        return [self._flair.predict(sentence) for sentence in text]

    def torchmoji(self, text: InputType, top_n: int) -> list[list[str]]:
        """Evaluate a single text or a list of texts through the TorchMoji model"""
        if isinstance(text, str):
            text = [text]
        return [self._torchmoji.predict(sentence, top_n=top_n) for sentence in text]
