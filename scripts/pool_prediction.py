from wordsmyth import Wordsmyth
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

ws = Wordsmyth()
texts = [["Hello world"] * 5] * 5

if __name__ == "__main__":
    with ThreadPoolExecutor(len(texts)) as pool:
        flair = pool.map(ws.flair, texts)
        torchmoji = pool.map(ws.torchmoji, texts, repeat(10))
        for resf, rest in zip(flair, torchmoji):
            print(resf, rest)
        #for flair, torch in zip(pool.map(ws.flair, texts), pool.map(ws.torchmoji, texts, repeat(10))):
        #    print(flair, torch)
