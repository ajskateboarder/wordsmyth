"""API route to predict sentiment of text"""

from typing import List

from fastapi import APIRouter, Header

from src.micro.models.emojis import Emoji
from . import emoji

router = APIRouter()


@router.post("/deepmoji/predict", response_model=List[Emoji])
def read(texts: List[str]):
    emojis = []

    for text in texts:
        res = emoji.predict(text)
        emojis.append({"emojis": res, "text": text})

    return emojis
