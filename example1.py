from src.ytd import get_comments

from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

session = FuturesSession()

print("getting comments")
texts = [i for i in get_comments("x7gaqhF-wrQ", 100)]
print(len(texts))


def chunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


chunks = list(chunk(texts, 20))

futures = [
    session.get(
        f"http://localhost:800{i}/predict", headers={"texts": str(c).encode("utf-8")}
    )
    for i, c in zip(list(range(6))[1:], chunks)
]

for future in as_completed(futures):
    resp = future.result()
    print(resp.json())
