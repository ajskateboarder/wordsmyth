from pydantic import BaseModel, HttpUrl


class YTComment(BaseModel):
    cid: str
    content: str
    time: str
    author: str
    channel: str
    likes: int
    avatar: HttpUrl
    heart: bool
