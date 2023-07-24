#!/usr/bin/python3
import sqlite3

from scipy.stats import ttest_rel
from sklearn.metrics import accuracy_score
import pandas as pd

from markdown import markdown
from markdown.extensions.tables import TableExtension

pd.options.mode.chained_assignment = None

conn = sqlite3.connect("reviews.sqlite")
tables = list(
    map(
        lambda x: x[0],
        pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn).values,
    )
)

print(
    """<link rel="stylesheet" href="github.css" />
<div class="markdown-body">
<h1>Results</h1>
p < 0.05 indicates significance
"""
)
for item in tables:
    print(f"<h2>{item}</h2>")
    df = pd.read_sql(f"SELECT * from {item}", conn)
    df.dropna(inplace=True)

    print(markdown(f"**amazon rating**: {round(df.actual.mean(), 2)}\n"))
    print(markdown(f"**wordsmyth rating**: {round(df.prediction.mean(), 2)}"))

    table = df.sample(5)
    table.text = table.text.apply(lambda x: f"{x.strip()[:100]}...")
    table = table.to_markdown(index=False)
    print(markdown(table, extensions=[TableExtension()]))

    t, p = ttest_rel(list(df.actual), list(map(float, list(df.prediction))))
    print(
        markdown(
            f"\n**p-value**: {p:.5f} ({'significant' if p < 0.05 else 'not significant'})\n"
        )
    )
    score = accuracy_score(df.actual.to_list(), df.prediction.to_list())
    print(markdown(f"**accuracy score**: {score}"))
print("</div>")
