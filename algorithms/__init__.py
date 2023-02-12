from __future__ import annotations

from .flair import Flair
from .torchmoji import TorchMoji

flair = Flair()
torch = TorchMoji()

def predict_flair(texts: list[str]):
    for text in texts:
        yield {"sentiment": flair.predict(text), "text": text}

def predict_torchmoji(texts: list[str], emojis: int):
    for text in texts:
        yield {"emojis": torch.predict(text, top_n=emojis), "text": text}
