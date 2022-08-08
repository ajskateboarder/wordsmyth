import streamlit as st
import requests

from src.ytd import get_comments
from src.deepmoji import Emojize

emoji = Emojize()

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

        comments = get_comments(yt_id)
        for comment in comments:
            st.write(comment, emoji.predict(comment))
