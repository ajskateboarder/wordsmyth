import pandas as pd
from sklearn.metrics import f1_score

df = pd.read_json("benchmark.json", lines=True)
df = df[df["predicted"] == df["predicted"]]

true = df["actual"].to_list()
pred = df["predicted"].map(lambda x: round(min(5, x * 10))).to_list()
print(true, len(true))
print(pred, len(pred))


print("F1 accuracy:", f1_score(true, pred, average="micro"))
