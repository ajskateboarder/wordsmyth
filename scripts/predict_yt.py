import pandas as pd
from wordsmyth import Pipeline


def preprocess_text(item: str) -> str:
    return item.encode("utf-16", "surrogatepass").decode("utf-16").strip()


df = pd.read_json("comments.json", lines=True)
df["commentText"].apply(preprocess_text)

text = [
    text
    for text, videoId in zip(df["commentText"], df["videoId"])
    if videoId == "Y3HLI6h7_U4"
]
print(text)

pipe = Pipeline()
ratings = []

for item in pipe.predict_parallel(text):
    ratings.append(item.rating())
    print(f"{item.text}: {item.rating()}")

print()
