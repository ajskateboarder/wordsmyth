"""
Comment collection wrapper built with a stolen YT Data API key
"""
import requests

KEY = "AIzaSyAyYPux1VOpcbKk2V_FKt3nPxfz6lu437k"


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
    return [
        item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        for item in req.json()["items"]
    ]
