import wordsmyth

w = wordsmyth.Wordsmyth()
print(w._flaircb([["Hello"] * 5]))
print(w.model_eval([["Hello"] * 5], emojis=10))
