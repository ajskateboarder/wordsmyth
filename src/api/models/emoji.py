from pydantic import BaseModel


class Emoji(BaseModel):
    emoji: str
    repr: str
    text: str
