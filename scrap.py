from random import choice
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import time
import json

import requests
from youtube_comment_downloader import YoutubeCommentDownloader

session = requests.Session()
session.headers = {
    "User-Agent": choice(
        [
            "Mozilla/5.0 (X11; CrOS aarch64 14816.131.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        ]
    )
}

req = session.get("https://youtube.com/")
yt = YoutubeCommentDownloader()

INIT_DATA = r'(?:window\s*\[\s*["\']ytInitialData["\']\s*\]|ytInitialData)\s*=\s*({.+?})\s*;\s*(?:var\s+meta|</script|\n)'
CONFIG = r"ytcfg\.set\s*\(\s*({.+?})\s*\)\s*;"


def search_dict(partial, search_key):
    stack = [partial]
    while stack:
        current_item = stack.pop()
        if isinstance(current_item, dict):
            for key, value in current_item.items():
                if key == search_key:
                    yield value
                else:
                    stack.append(value)
        elif isinstance(current_item, list):
            for value in current_item:
                stack.append(value)


def ajax_request(endpoint, ytcfg, retries=5, sleep=20):
    url = (
        "https://www.youtube.com"
        + endpoint["commandMetadata"]["webCommandMetadata"]["apiUrl"]
    )

    keys = {
        "context": ytcfg["INNERTUBE_CONTEXT"],
        "continuation": endpoint["continuationCommand"]["token"],
    }

    for _ in range(retries):
        response = session.post(
            url, params={"key": ytcfg["INNERTUBE_API_KEY"]}, json=keys
        )
        if response.status_code == 200:
            return response.json()
        if response.status_code in [403, 413]:
            return {}
        else:
            time.sleep(sleep)


def regex_search(text, pattern, group=1, default=None):
    match = re.search(pattern, text)
    return match.group(group) if match else default


data = json.loads(regex_search(req.text, INIT_DATA))
ids = [
    vid
    for video in search_dict(data, "richItemRenderer")
    if (vid := video["content"].get("videoRenderer", {}).get("videoId"))
    if vid is not None
]

config = json.loads(regex_search(req.text, CONFIG))
route = next(search_dict(data, "continuationItemRenderer"))["continuationEndpoint"]

while route is not None:
    data = ajax_request(route, config)
    more = []
    for video in search_dict(data, "richItemRenderer"):
        try:
            vid = video["content"]["videoRenderer"]["videoId"]
            more.append(vid)
        except KeyError:
            pass
    ids.extend(more)

    route = next(search_dict(data, "continuationItemRenderer"), {}).get(
        "continuationEndpoint"
    )

with open("output.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(ids))

# def print_comments(vid):
#     for comment, _ in zip(
#         yt.get_comments_from_url(f"https://youtube.com/watch?v={vid}", sort_by=0),
#         range(10),
#     ):
#         print(comment["text"])


# futures = []
# with ThreadPoolExecutor() as executor:
#     for i in ids[:20]:
#         futures.append(executor.submit(print_comments, vid=i))

# for fut in as_completed(futures):
#     print(fut.result())
#     time.sleep(2)
