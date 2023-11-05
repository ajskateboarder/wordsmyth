import json
import sys

from wordsmyth.pipeline import Pipeline
from wordsmyth.rate import ReviewRater

print("firing up model")

p = Pipeline()
thing = p(" ".join(sys.argv[1:]))

with open("src/wordsmyth/data/emojimap.json", encoding="utf-8") as fh:
    emojimap = json.load(fh)
based = ReviewRater(thing, emojimap)

print(thing)
based.fix_content()
based.flag()
print(based.flags)
print(based.rate())
