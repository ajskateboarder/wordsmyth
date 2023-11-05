from __future__ import annotations

import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Generator, Union, Optional

from .models import Flair, TorchMoji
from .items import Sentiment, Output, Int, Float


Rating = Optional[Union[Int, Float]]


class Pipeline:
    """Wordsmyth text rating pipeline"""

    def __init__(self) -> None:
        warnings.filterwarnings("ignore")

        self._flair = Flair()
        self._torchmoji = TorchMoji()

    def __call__(
        self, text: str, ting: bool = False, emojis: int = 10
    ) -> Union[Output, Rating]:
        """Predict the star rating for a single content"""
        torchmoji = self._torchmoji.predict(text, emojis)
        flair = self._flair.predict(text)
        output = Output(sentiment=Sentiment(**flair), emojis=torchmoji, text=text)  # type: ignore
        try:
            return output.rating() if ting else output
        except AttributeError:
            return None
