import json
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from wordsmyth import Pipeline


def preprocess_text(item: str) -> str:
    return item.replace(
        "                    The media could not be loaded.\n                ", ""
    ).strip()


df = pd.read_json("reviews.json", lines=True)
df["reviewText"].apply(preprocess_text)

text = df["reviewText"].to_list()

text_rate_map = dict(zip(df["reviewText"].to_list(), df["overall"].to_list()))

pipe = Pipeline()


def evaluate_text(sentence):
    try:
        return pipe.eval(sentence)
    except AttributeError:
        return None


with ThreadPoolExecutor() as pool:
    results = pool.map(evaluate_text, text[:200])
    for result in results:
        try:
            print_obj = {
                "reviewText": result.text,
                # This can possibly error
                "predicted": result.rating(),
                "actual": text_rate_map[result.text],
            }
        except AttributeError:
            print_obj = {
                "reviewText": result.text,
                "predicted": None,
                "actual": text_rate_map[result.text],
            }
        print(json.dumps(print_obj))
