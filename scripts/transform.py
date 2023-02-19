import pandas as pd

data = pd.read_json("comments.json").to_dict(orient="records")
items = sum([list(e for e in d[0] if e is not None) for d in data], [])
df = pd.DataFrame(items).set_axis(["reviewText", "overall"], axis=1)
df.to_json("comments_fixed.json", orient="records")