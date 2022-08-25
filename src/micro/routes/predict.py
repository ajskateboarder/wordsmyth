"""API route to predict emojis"""

from typing import List
import ast

from fastapi import APIRouter, Header

from . import emoji
from src.micro.models.emojis import Emoji

router = APIRouter()


@router.get("/predict", response_model=List[Emoji])
def read(texts: list = Header()):
    emojis = []
    texts = ast.literal_eval(list(texts)[0])

    for text in texts:
        res = emoji.predict(text)
        emojis.append({"emoji": res, "text": text})

    return emojis
