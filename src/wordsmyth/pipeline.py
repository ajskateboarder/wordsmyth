from __future__ import annotations

import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Generator, Union, Optional, Any

from .models.flair import Flair
from .models.torchmoji import TorchMoji
from .items import Sentiment, Output


Rating = Optional[Union[int, float]]


def divide_list(array: list, num: int) -> Generator[list, None, None]:
    """Divide a list into even chunks"""
    for i in range(0, len(array), num):
        yield array[i : i + num]


class Pipeline:
    """Wordsmyth text rating pipeline"""

    def __init__(self) -> None:
        warnings.filterwarnings("ignore")

        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def predict(
        self, text: str, emojis: int = 10, as_object: bool = False
    ) -> Union[Output, Rating]:
        """Predict the star rating for a single content"""
        torchmoji = self._torchmoji.predict(text, emojis)
        flair = self._flair.predict(text)
        output = Output(sentiment=Sentiment(**flair), emojis=torchmoji, text=text)  # type: ignore
        return output if as_object else output.rating()

    def predict_parallel(
        self, texts: list[str], emojis: int = 10
    ) -> Generator[Output, None, None]:
        """Predict star ratings for multiple contents.
        - This uses concurrent.futures.ThreadPoolExecutor.
        - This only returns data objects which makes it easier to track which content was rated
        """
        with ThreadPoolExecutor() as pool:
            futures = [
                pool.submit(self.predict, text, emojis, as_object=True)
                for text in texts
            ]
            for future in as_completed(futures):
                yield future.result()
