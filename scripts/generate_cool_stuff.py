from __future__ import annotations
from typing import Callable

from functools import partial
import sqlite3
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

conn = sqlite3.connect("new_reviews.sqlite")
query: Callable[[str], pd.DataFrame] = partial(pd.read_sql_query, con=conn)

tables = []

for table in query("SELECT name FROM sqlite_master WHERE type='table';").itertuples():
    dff = query(f"SELECT * from {table.name}")
    dff.dropna(inplace=True)
    tables.append(dff)

y_values = []
counts = []

pd.concat(tables).to_csv("h.csv")

for i in range(1, 6):
    df = pd.concat(tables).query(f"actual == {i}")
    print(accuracy_score(df.actual.to_list(), df.prediction.to_list()))
    y_values.append(accuracy_score(df.actual.to_list(), df.prediction.to_list()))
    counts.append(len(df.actual))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.bar(list(map(lambda i: f"{i} stars", range(1, 6))), counts)

ax1.xaxis.set_label("Star rating")
ax1.yaxis.set_label("# of reviews")

ax2.set_title("# of reviews")

ax2.bar(list(map(lambda i: f"{i} stars", range(1, 6))), y_values)
ax2.set_yticklabels([f"{x:,.0%}" for x in ax2.get_yticks()])

ax2.xaxis.set_label("Star rating")
ax2.yaxis.set_label("Accuracy score")

ax2.set_title("Star prediction accuracy")
plt.tight_layout()
plt.savefig("hello22.png")
