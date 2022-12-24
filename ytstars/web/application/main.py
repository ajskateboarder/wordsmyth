from functools import lru_cache
import io
import json

import yaml
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import requests

from ytstars.web.queue.rpc import ProcessRPC
from ytstars.web.application.models import Queue
from ytstars.web.application.sse import SSE

rpc = ProcessRPC()
announcer = SSE()

app = FastAPI(
    title="YTStars API",
    description=(
        "This API provides easy support to queue videos of your choice to get them automatically rated. "
        "You can generate a typesafe client with the provided OpenAPI schema or use the tRPC client if you use TypeScript"
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def id_exists(video):
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


def stream():
    messages = announcer.listen()
    while True:
        msg = messages.get()
        yield msg
        if msg == "0":
            break


async def cool_route(request: Request):
    """Server-sent-events template route to be dynamically registered"""
    status_generator = stream()
    return EventSourceResponse(status_generator)


def send_status(request: Request):
    """Pass a live status from the backend through a SSE"""
    msg = request.headers["Status"]
    print(f"MESSAGE: {msg}")
    if not msg in ("1", "1>done", "2", "2>done", "0"):
        return 400
    if msg == "0":
        path = "/" + str(request.url).replace(str(request.base_url), "")
        paths = [e.path for e in app.routes]
        if path in paths:
            url_object = app.routes[paths.index(path)]
            app.routes.remove(url_object)

    announcer.announce(msg=msg)
    return {}, 200


@app.post(
    "/queue",
    response_model=Queue.Output,
    name="Submission queue",
    operation_id="queue",
    tags=["queue"],
)
async def post_submit(response: Response, video: Queue.Input):
    """Queue a video ID for processing and generate a live status route"""
    try:
        video_id = video.video_id
    except json.decoder.JSONDecodeError:
        response.status_code = 404
        return {"status": "fail", "data": {"message": "Video ID not supplied"}}

    if not id_exists(video_id):
        response.status_code = 404
        return {"status": "fail", "data": {"message": "Video does not exist"}}

    queue = json.loads(rpc.call(video_id).decode())
    print(queue)
    app.add_api_route(queue["listener"], cool_route)
    app.add_api_route(f"{queue['listener']}/send", send_status)

    if queue["status"] == "exists":
        response.status_code = 400
        return {
            "status": "fail",
            "data": {
                "queue": queue["state"],
                "message": "Video already exists in queue. Please check back later",
            },
        }

    return {
        "status": "success",
        "queue": queue,
        "data": {
            "message": "Video is now in the submission queue.",
            "queue": queue["state"],
            "listener": queue["listener"],
        },
    }
