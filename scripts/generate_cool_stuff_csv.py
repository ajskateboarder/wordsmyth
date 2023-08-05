from __future__ import annotations
import warnings
import sys

import pandas as pd

import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

warnings.filterwarnings("ignore")


def my_accuracy(actual: list, predicted: list) -> float:
    count = 0
    for a, p in zip(actual, predicted):
        if p in (a - 1, a, a + 1):
            count += 1
    return count / len(actual)


y_values = []
yish_values = []
counts = []

table = pd.read_csv(sys.argv[1])
table["prediction"] = table["prediction"].map(lambda x: max(0, x))
table.dropna(inplace=True)

print(accuracy_score(table.actual.to_list(), table.prediction.to_list()))
print(my_accuracy(table.actual.to_list(), table.prediction.to_list()))

for i in range(1, 6):
    df = table.query(f"actual == {i}")
    y_values.append(accuracy_score(df.actual.to_list(), df.prediction.to_list()))
    yish_values.append(my_accuracy(df.actual.to_list(), df.prediction.to_list()))
    counts.append(len(df.actual))

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5))

ax1.bar(list(map(lambda i: f"{i} stars", range(1, 6))), counts)
ax1.set_title("Number of reviews per category")
ax1.set_ylabel("# of reviews")
ax1.set_xlabel("Star category")

ax2.bar(list(map(lambda i: f"{i} stars", range(1, 6))), y_values)
ax2.set_title("Plain accuracy per category")
ax2.set_yticklabels([f"{x:,.0%}" for x in ax2.get_yticks()])
ax2.set_ylabel("Accuracy %")
ax2.set_xlabel("Star category")

ax3.bar(
    list(map(lambda i: f"{i} stars", range(1, 6))),
    yish_values,
)
ax3.set_title("One-off accuracy per category")
ax3.set_yticklabels([f"{x:,.0%}" for x in ax3.get_yticks()])
ax3.set_ylabel("Accuracy %")
ax3.set_xlabel("Star category")

ax1.tick_params(axis="x", rotation=45)
ax2.tick_params(axis="x", rotation=45)
ax3.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig(sys.argv[2])
