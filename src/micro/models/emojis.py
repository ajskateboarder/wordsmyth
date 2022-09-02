from typing import List

from typing_extensions import TypedDict


class Emoji(TypedDict):
    emojis: List[str]
    text: str
