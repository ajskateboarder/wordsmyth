from pydantic import BaseModel, Field


class Input(BaseModel):
    video_id: str = Field(title="dQw4w9WgXcQ")


from pydantic import create_model

Input = create_model("Input", video_id=(str, ...))
