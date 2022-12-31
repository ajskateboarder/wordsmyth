from typing import List, Optional
from pydantic import BaseModel, Field


class Queue:
    class Output(BaseModel):
        class Data(BaseModel):
            message: str = Field(title="Extended description of what happened")
            listener: Optional[str] = Field(title="Websocket URL to receive status")

        status: str = Field(title="success | reject")
        data: Data = {}

    class Input(BaseModel):
        video_id: str = Field(title="dQw4w9WgXcQ")
