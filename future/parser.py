from typing import List

from pydantic import BaseModel


class Sentiment(BaseModel):
    neg: float
    neu: float
    pos: float


class ResponseItem(BaseModel):
    sentiment: Sentiment
    text: str


class Model(BaseModel):
    response: List[ResponseItem]
