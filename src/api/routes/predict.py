from typing import List

from fastapi import APIRouter, Header

from . import emoji
from src.api.models.emoji import Emoji

router = APIRouter()


@router.get("/predict", response_model=List[Emoji])
def read(texts: list = Header()):
    emojis = []
    texts = texts[0].strip("][").split(", ")

    for text in texts:
        res = emoji.predict(text)
        emojis.append({"emoji": res[0], "repr": res[1], "text": text})
    return emojis
