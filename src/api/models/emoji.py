from pydantic import BaseModel


class Emoji(BaseModel):
    emoji: str
    text: str
