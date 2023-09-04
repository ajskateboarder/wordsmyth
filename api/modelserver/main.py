from functools import lru_cache
import os
import time
import json

import redis

from wordsmyth import Pipeline

db = redis.StrictRedis(host=os.environ.get("REDIS_HOST"))

@lru_cache()
def model():
    return Pipeline()

def prediction_process():
    while True:
        with db.pipeline() as pipe:
            pipe.lrange(os.environ.get("TEXT_QUEUE"), -1, -1)
            e = pipe.execute()
            if e == [[]]:
                continue
            text = json.loads(e[0][0].decode("utf-8"))
        db.set(text["id"], model()(text))

        time.sleep(float(os.environ.get("SERVER_SLEEP")))

if __name__ == "__main__":
    prediction_process()
