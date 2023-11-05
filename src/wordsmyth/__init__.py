from functools import lru_cache
import warnings
import json

from wordsmyth.rate import ReviewRater
from wordsmyth.items import Output
from wordsmyth.constants import DIR_PATH

@lru_cache(maxsize=None)
def _models():
    from wordsmyth.models import Flair, TorchMoji
    return Flair(), TorchMoji()

@lru_cache(maxsize=None)
def _emojimap():
    with open(f"{DIR_PATH}/data/emojimap.json", encoding="utf-8") as emojimap:
        return json.load(emojimap)

def rate(text: str, *, emojis: int = 10, rounded: bool = True) -> int | float:
    """Assign a star rating to text"""
    warnings.filterwarnings("ignore")
    flair, torch = _models()
    output = Output(sentiment=flair.predict(text), emojis=torch.predict(text, emojis), text=text)
    rater = ReviewRater(output, _emojimap())

    rater.fix_content()
    rater.flag()

    return rater.rate(rounded)
