from typing import List, Union

from fastapi import APIRouter, Header

from . import emoji
from src.api.models.emojis import Emojis

router = APIRouter()


@router.get("/predict", response_model=Emojis)
def read(texts: list = Header()):
    emojis = []
    texts = texts[0].strip("][").split(", ")

    for text in texts:
        res = emoji.predict(text)
        emojis.append({"emoji": res, "text": text})

    emojis = {
        "emojis": emojis,
        "alltext": " ".join([e["text"] for e in emojis]).replace("  ", " "),
    }

    return emojis
