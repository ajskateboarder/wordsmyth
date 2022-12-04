from fastapi import FastAPI, Response
from fastapi.responses import Response as Send
from functools import lru_cache
import requests
import json
import yaml
import io

from ..queue.rpc import VideoProcessingState
from .models import Queue

rpc = VideoProcessingState()
app = FastAPI()


def id_exists(video):
    req = requests.get(
        f"https://youtube.com/oembed?url=https://youtube.com/watch?v={video}",
        timeout=10,
    )
    return req.status_code == 200


@app.get("/openapi.yaml", include_in_schema=False)
@lru_cache()
def read_openapi_yaml() -> Send:
    openapi_json = app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Send(content=yaml_s.getvalue(), media_type="text/yaml")


@app.post(
    "/queue",
    response_model=Queue.Output,
    name="queue",
    description="Queue a video ID for processing",
    operation_id="queue",
)
async def post_submit(response: Response, video: Queue.Input):
    try:
        video_id = video.video_id
    except json.decoder.JSONDecodeError:
        response.status_code = 404
        return {"status": "reject", "message": "Video ID not supplied"}

    if not id_exists(video_id):
        response.status_code = 404
        return {"status": "reject", "message": "Video does not exist"}
    queue = json.loads(rpc.call(video_id).decode())

    if queue["status"] == "exists":
        response.status_code = 400
        return {
            "status": "reject",
            "message": "Video already exists in queue. Please check back later",
            "data": {
                "queue": queue["state"],
            },
        }

    return {
        "status": "success",
        "message": "Video is now in the submission queue",
        "data": {
            "queue": queue["state"],
        },
    }
