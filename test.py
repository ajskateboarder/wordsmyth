import requests

data = requests.post(
    "http://localhost:8081/youtube/queue", json={"video_id": "Rg8-9nc-y-U"}
)
print(data.json())
