from functools import lru_cache
import io
import json

import yaml
import requests

from redis import Redis
from rq import Queue

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import create_model

app = FastAPI(
    title="Wordsmith API",
    description=(
        "This API provides easy support to queue content of your choice to get them automatically rated. "
        "You can generate a typesafe client with the provided OpenAPI schema"
    ),
)

redis = Redis()
q = Queue(connection=redis)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def id_exists(video: str) -> bool:
    req = requests.get(
        f"https://youtube.com/oembed?url=https://youtube.com/watch?v={video}",
        timeout=10,
    )
    return req.status_code == 200


@app.get("/openapi.yaml", include_in_schema=False)
@lru_cache()
def read_openapi_yaml() -> Response:
    openapi_json = app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(content=yaml_s.getvalue(), media_type="text/yaml")


@app.post(
    "/youtube/queue",
    name="Submission queue",
    operation_id="queue",
    tags=["queue"],
)
async def post_submit(
    response: Response, video: create_model("Input", video_id=(str, ...))
):
    """Queue a YouTube video ID for processing"""

    if not id_exists(video.video_id):
        response.status_code = 404
        return {"status": "fail", "data": {"message": "Video does not exist"}}

    result = q.enqueue("wordsmith.web.store.queue_youtube", "G6STB2nC5Lg")

    return {"status": "success"}
