from concurrent.futures import as_completed
import json
import streamlit as st

from requests_futures.sessions import FuturesSession

from src.ytd import get_comments


def chunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


session = FuturesSession()

with st.form("form"):
    yt_id = st.text_input("YouTube video ID")

    submitted = st.form_submit_button()
    if submitted:
        res = session.get(
            f"https://youtube.com/oembed?url=https://youtube.com/watch?v={yt_id}"
        ).result()
        if res.status_code == 400:
            st.error("Video doesn't exist. Try a working video ID.")

        title = res.json()["title"]
        st.write(f'Downloading comments for "{title}". Please wait...')

        texts = [i for i in get_comments(yt_id, 100)]
        chunks = list(chunk(texts, 20))

        futures = [
            session.get(
                f"http://localhost:800{i}/predict",
                headers={"texts": str(c).encode("utf-8")},
            )
            for i, c in zip(list(range(6))[1:], chunks)
        ]

        res = []
        
        for future in as_completed(futures):
            resp = future.result().json()
            for re in resp:
                res.append([re["text"], re["emoji"]])

        with open('data.json', 'w') as fh:
            json.dump(res, fh)
