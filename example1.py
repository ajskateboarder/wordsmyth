from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

session = FuturesSession()
texts = [
    "Metamanrb was so dedicated to verifying this, truly motivational",
    "imagine seeing the attempt he got 89 but not the verification attempt",
    "i never realized that a good gameplay dual exists to the song Never Gonna Give You Up",
    "I never actually expected this level to get recognition what lmao",
    "The most legendary extreme demon in the game",
    "Definitely one of the levels of all time",
    "i went insane when i heard high stakes in this level for the first time",
    "Meta Processing By DankManRB, Verified By Rick Astley.",
    "Absolute banger level...overall gameplay seems pretty fun except that last ship",
    "This was surely an experience to watch",
]


def chunk(xs, n):
    n = max(1, n)
    return (xs[i : i + n] for i in range(0, len(xs), n))


chunks = list(chunk(texts, 2))

futures = [
    session.get(f"http://localhost:8001/predict", headers={"texts": str(chunks[0])})
]

for future in as_completed(futures):
    resp = future.result()
    print(resp.text)
