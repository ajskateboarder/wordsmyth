from pydantic import BaseModel, AnyHttpUrl


class YTComment(BaseModel):
    cid: str
    content: str
    time: str
    author: str
    channel: str
    likes: int
    avatar: str
    heart: bool
