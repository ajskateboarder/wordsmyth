from typing import List

from fastapi import APIRouter, Header

from . import emoji
from src.api.models.emoji import Emoji

router = APIRouter()


@router.get("/predict", response_model=List[Emoji])
def read(text: str = Header()):
    res = emoji.predict(text)
    return {"emoji": res[0], "repr": res[1]}
