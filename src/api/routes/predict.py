from typing import List, Union

from fastapi import APIRouter, Header

from . import emoji
from src.api.models.emoji import Emoji

router = APIRouter()


@router.get("/predict")
def read(texts: list = Header()):
    emojis = []
    texts = texts[0].strip("][").split(", ")

    for text in texts:
        res = emoji.predict(text)
        emojis.append({"emoji": res, "text": text})
    return emojis
