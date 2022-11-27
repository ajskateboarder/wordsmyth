from fastapi import FastAPI
import requests

from .rpc import VideoExistsClient

rpc = VideoExistsClient()
app = FastAPI()


def id_exists(video):
    req = requests.get(
        f"https://youtube.com/oembed?url=https://youtube.com/watch?v={video}",
        timeout=10,
    )
    return req.status_code == 200


@app.get("/submit")
def root(video_id: str):
    if not id_exists(video_id):
        return {"status": "reject", "message": "Video does not exist"}
    response = rpc.call(video_id).decode()
    if response == "exists":
        return {
            "status": "reject",
            "message": "Video already in queue. Please check back later",
        }
    return {
        "status": "success",
        "message": "Please wait while processing is done...",
    }
