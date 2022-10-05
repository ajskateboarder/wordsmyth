from typing import List

from pydantic import BaseModel


class Sentiment(BaseModel):
    sentiment: str
    score: float


class ResponseItem(BaseModel):
    sentiment: Sentiment
    text: str


class Model(BaseModel):
    response: List[ResponseItem]
