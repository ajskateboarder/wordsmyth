from concurrent.futures import ThreadPoolExecutor, as_completed

import streamlit as st
import requests
import grpc

from micro.stubs.server_pb2 import Sentiments, Texts
from micro.stubs.server_pb2_grpc import ModelStub

from ytd import get_comments


def chunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


print("Connecting to gRPC server")
channel = grpc.insecure_channel("localhost:50051")

with st.form("form"):
    yt_id = st.text_input("YouTube video ID")

    submitted = st.form_submit_button()
    if submitted:
        res = requests.get(
            f"https://youtube.com/oembed?url=https://youtube.com/watch?v={yt_id}"
        )
        if res.status_code == 400:
            st.error("Video doesn't exist. Try a working video ID.")

        title = res.json()["title"]
        st.write(f'Downloading comments for "{title}". Please wait...')

        comments = [i for i in get_comments(yt_id, 200) if i["reply"] == False]
        content = [i["text"] for i in comments]

        chunks = list(chunk(content, 100))

        fetch = ModelStub(channel).torchmoji
        print("Requesting comments")

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch, Texts(texts=v)) for v in chunks]

        for f in as_completed(futures):
            print("Collected")
            print(f.result())


# main([["This is the shit!", "You are shit."], ["Nice", "Very cool"]])
