import pandas as pd
from algo.deepmoji import Emojize

e = Emojize()

df = pd.read_csv("./future/extracts.csv")
texts = df["text"].head(100)

def func(x):
    return e.predict(x)

print(list(zip(texts.to_list(), texts.apply(func).to_list())))
