from fastapi import FastAPI, Request
import requests

from .queue.rpc import VideoProcessingState

rpc = VideoProcessingState()
app = FastAPI()


def id_exists(video):
    req = requests.get(
        f"https://youtube.com/oembed?url=https://youtube.com/watch?v={video}",
        timeout=10,
    )
    return req.status_code == 200


@app.post("/submit")
async def submit(request: Request):
    video_id = (await request.json())["video_id"]
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
        "message": "Video is now in the submission queue",
    }
