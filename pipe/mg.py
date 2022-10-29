#!/usr/bin/env python3

import sys
import ast

inputs = list(sys.stdin)

flair = ast.literal_eval(inputs[0].strip())
torch = ast.literal_eval(inputs[-1])

merged = [dict(t, **f) for t, f in zip(torch, flair)]

print("sentiment,score,text,emojis")
for m in merged:
    print(f"{m['sentiment']['sentiment']},{m['sentiment']['score']},'{m['text']}','{','.join(m['emojis'])}'")
