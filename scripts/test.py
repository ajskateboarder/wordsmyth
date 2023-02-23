from wordsmyth import Wordsmyth

ws = Wordsmyth()
ws.model_eval([["Hello world!"] * 5, ["This sucks!"] * 5])