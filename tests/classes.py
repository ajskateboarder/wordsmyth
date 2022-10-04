from typing import Literal, List
from pydantic import BaseModel


class Flair(BaseModel):
    sentiment: Literal["pos", "neu", "neg"]
    score: float
    text: str


class Torch(BaseModel):
    emojis: List[str]
    text: str


class TR(BaseModel):
    emoji: str
    repr: str
