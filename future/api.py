from fastapi import FastAPI
import uvicorn

from utils.comments import download_comments
from algo.wrapper import request

app = FastAPI(debug=True)


@app.get("/queue")
def queue(vid: str):
    comments = download_comments(vid, 100)
    tmres = request(comments, "torchmoji", count=10)
    flres = request(comments, "flair")

    return [dict(t, **f) for t, f in zip(tmres, flres)]


uvicorn.run(app)
