from wordsmyth import Wordsmyth
import json

with open("comments.json", encoding="utf-8") as fh:
    comments = json.load(fh)

ws = Wordsmyth()
comments = ws.eval(comments, 10)

for comment in comments:
    try:
        print(comment.text, comment.rate())
    except AttributeError:
        pass
