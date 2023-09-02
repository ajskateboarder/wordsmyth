from websockets.sync.client import connect
import json

with connect("ws://localhost:8001", max_size=None) as ws:
    ws.send(
        json.dumps(
            {
                "command": "login",
                "username": "the.mystic.6660@gmail.com",
                "password": "adiiscool74@",
            }
        )
    )
    ws.send(json.dumps({"command": "scrape", "asin": "B008I7TNDW"}))
    while True:
        print(ws.recv())
