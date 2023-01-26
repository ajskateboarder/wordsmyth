"""Content queuing with RQ workers"""

import time
import requests

from utils.comments_v3 import download_comments
from algorithms.wrapper import request


def queue_youtube(video_id):
    """Queue a YouTube video with its ID"""

    start = time.time()
    comments = download_comments(video_id, 10)

    tmres = request(comments, "torchmoji", count=10)
    flres = request(comments, "flair")
    result = [dict(t, **f) for t, f in zip(tmres, flres)]
    print({"output": result, "time": time.time() - start})

    return {"output": result, "time": time.time() - start}
