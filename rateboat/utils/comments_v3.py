"""
Comment collection wrapper built with a stolen YT Data API key
"""
import requests

KEY = "AIzaSyDfaS4lcSHVwbZ_p3NhTqT3tQNAfeaKQtk"


def chunks(l, n):
    for i in range(0, n):
        yield l[i::n]


def download_comments(video_id, limit):
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
