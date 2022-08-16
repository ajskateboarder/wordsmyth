from typing_extensions import TypedDict
from typing import List

from pydantic import BaseModel


class Emoji(TypedDict):
    emoji: str
    text: str


class Emojis(BaseModel):
    emojis: List[Emoji]
    alltext: str
