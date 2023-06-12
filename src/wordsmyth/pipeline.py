from __future__ import annotations

import warnings
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from typing import Generator, Union

from .models.flair import Flair
from .models.torchmoji import TorchMoji
from .items import Sentiment, Output

InputType = Union[str, "list[str]"]


def divide_list(array: list, num: int) -> Generator[list, None, None]:
    """Divide a list into even chunks"""
    for i in range(0, len(array), num):
        yield array[i : i + num]


class Pipeline:
    """Efficient Wordsmyth text rating pipeline
    ```
    >>> from wordsmyth import Pipeline
    >>> Pipeline().eval("LOL").rating()
    0.5
    ```
    ```
    >>> from wordsmyth import Pipeline
    >>> [e.rating() for e in Pipeline().eval(["Not as great", "LOL"])]
    [0.1, 0.5]
    ```
    """

    def __init__(self) -> None:
        warnings.filterwarnings("ignore")
        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def eval(self, text: str, emojis: int = 10) -> Output:
        """Evaluate a text/list of text through both Flair and TorchMoji"""
        torchmoji = self._torchmoji.predict(text, emojis)
        flair = self._flair.predict(text)
        return Output(sentiment=Sentiment(**flair), emojis=torchmoji, text=text)
