"""
Youtube comment collection plugin
"""
from typing import List, Generator, Any
from dotenv import dotenv_values

import requests

config = dotenv_values(".env")
KEY = config["YT_KEY"]


def chunks(lis: List[Any], number: int) -> Generator[List[Any], None, None]:
    """List chunk helper"""
    for i in range(0, number):
        yield lis[i::number]


def download_comments(video_id: str, limit: int) -> List[List[str]]:
    req = requests.get(
        "https://www.googleapis.com/youtube/v3/commentThreads",
        timeout=10,
        params={
            "key": KEY,
            "part": "snippet",
            "maxResults": limit,
            "videoId": video_id,
        },
        headers={"Referer": "https://youtubecommentsdownloader.com"},
    )
    return list(
        item
        for item in chunks(
            [
                item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                for item in req.json()["items"]
            ],
            10,
        )
        if item != []
    )