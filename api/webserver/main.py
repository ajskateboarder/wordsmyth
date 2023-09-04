import os
import json
import uuid
import time

import redis

from fastapi import FastAPI, HTTPException
from starlette.requests import Request

app = FastAPI()
db = redis.StrictRedis(host=os.environ.get("REDIS_HOST"))

CLIENT_MAX_TRIES = int(os.environ.get("CLIENT_MAX_TRIES"))

@app.get("/")
def index():
    return "hi"

@app.post("/predict")
def predict(request: Request, text: str):
    response = {"success": False}

    if request.method == "POST":
        cid = str(uuid.uuid4())
        to_classify = {"text": text, "id": cid}
        db.rpush(os.environ.get("TEXT_QUEUE"), json.dumps(to_classify))

        num_tries = 0
        while num_tries < CLIENT_MAX_TRIES:
            num_tries += 1

            output = db.get(cid)

            if output is not None:
                output = output.decode("utf-8")
                response["predictions"] = json.loads(output)

                db.delete(cid)
                break
            
            time.sleep(float(os.environ.get("CLIENT_SLEEP")))
            response["success"] = True
        
    return response
