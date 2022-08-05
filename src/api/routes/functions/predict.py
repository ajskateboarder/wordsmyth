from fastapi import APIRouter, Header

from .. import emoji
from src.api.models.emoji import Emoji

router = APIRouter()


@router.get("/func/predict", response_model=Emoji)
def read(text: str = Header()):
    res = emoji.predict(text)
    return {"emoji": res[0], "repr": res[1]}
