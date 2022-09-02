from pydantic import BaseModel
from typing_extensions import TypedDict


class Roberta(TypedDict):
    text: str
    pos: float
    neu: float
    neg: float
