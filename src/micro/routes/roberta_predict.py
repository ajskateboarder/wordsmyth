"""API route to predict ROBERTA sentiment"""

from typing import List

from fastapi import APIRouter, Header

from src.micro.models.roberta import Roberta
from . import roberta

router = APIRouter()


@router.post("/roberta/predict", response_model=List[Roberta])
def read(texts: List[str]):
    sents = []

    for text in texts:
        sents.append({"text": text, **roberta.predict(text)})

    return sents
