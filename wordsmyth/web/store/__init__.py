"""Content queuing with RQ workers"""

import time

from wordsmyth.algorithms.wrapper import request
from wordsmyth.plugins.youtube import download_comments


def queue_youtube(video_id: str) -> dict:
    """Queue a YouTube video with its ID"""

    start = time.time()
    comments = download_comments(video_id, 10)

    tmres = request(comments, "torchmoji", count=10)
    flres = request(comments, "flair")
    result = [dict(t, **f) for t, f in zip(tmres, flres)]
    print({"output": result, "time": time.time() - start})

    return {"output": result, "time": time.time() - start}
