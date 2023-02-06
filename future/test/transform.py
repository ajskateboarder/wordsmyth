import pandas as pd
import json


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

df = pd.read_json("./Appliances_5.json", lines=True)
reviews = df[["reviewText", "overall"]].sort_values("overall", ascending=False)

df2 = pd.read_json("./data.json")
df.sort_values("reviewText")
df2.sort_values("content")
print(df[["reviewText", "overall"]].head())
print(df2["content"].head(), "\n")
df2["overall"] = df["overall"]
print(df2.to_json("data2.json", orient="records"))
# content = list(chunks(reviews["reviewText"].to_list(), 10))

# with open("reviews.json", "w", encoding="utf-8") as fh:
#     json.dump(content, fh)


