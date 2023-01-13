import requests

r = requests.post("http://localhost:8081/queue", json={"video_id": "8B20fRB78nA"})
print(r.json())