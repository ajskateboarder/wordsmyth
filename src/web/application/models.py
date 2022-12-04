from typing import List, Optional
from pydantic import BaseModel


class Queue:
    class Output(BaseModel):
        class Data(BaseModel):
            queue: List[str]

        status: str
        message: str
        data: Optional[Data] = {}

    class Input(BaseModel):
        video_id: str
