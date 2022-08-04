"""
Original script by https://github.com/ahmedshahriar
Refactored into a module
"""

import json
from os import path
import time

import pandas as pd
import requests

from .helpers import ajax_request, regex_search, search_dict


pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

YOUTUBE_COMMENTS_AJAX_URL = "https://www.youtube.com/comment_service_ajax"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
FILE_NAME = "ytb_comments.csv"
SORT_BY_POPULAR = 0

YT_CFG_RE = r"ytcfg\.set\s*\(\s*({.+?})\s*\)\s*;"
YT_INITIAL_DATA_RE = r'(?:window\s*\[\s*["\']ytInitialData["\']\s*\]|ytInitialData)\s*=\s*({.+?})\s*;\s*(?:var\s+meta|</script|\n)'


def download_comments(url, sort_by, language=None, sleep=0.1):
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    response = session.get(url)

    if "uxe=" in response.request.url:
        session.cookies.set("CONSENT", "YES+cb", domain=".youtube.com")
        response = session.get(url)

    html = response.text
    ytcfg = json.loads(regex_search(html, YT_CFG_RE, default=""))
    if not ytcfg:
        return  # Unable to extract configuration
    if language:
        ytcfg["INNERTUBE_CONTEXT"]["client"]["hl"] = language

    data = json.loads(regex_search(html, YT_INITIAL_DATA_RE, default=""))

    section = next(search_dict(data, "itemSectionRenderer"), None)
    renderer = (
        next(search_dict(section, "continuationItemRenderer"), None)
        if section
        else None
    )
    if not renderer:
        return

    needs_sorting = sort_by != SORT_BY_POPULAR
    continuations = [renderer["continuationEndpoint"]]
    while continuations:
        continuation = continuations.pop()
        response = ajax_request(session, continuation, ytcfg)

        if not response:
            break
        if list(search_dict(response, "externalErrorMessage")):
            raise RuntimeError(
                "Error returned from server: "
                + next(search_dict(response, "externalErrorMessage"))
            )

        if needs_sorting:
            sort_menu = next(
                search_dict(response, "sortFilterSubMenuRenderer"), {}
            ).get("subMenuItems", [])
            if sort_by < len(sort_menu):
                continuations = [sort_menu[sort_by]["serviceEndpoint"]]
                needs_sorting = False
                continue

        actions = list(search_dict(response, "reloadContinuationItemsCommand")) + list(
            search_dict(response, "appendContinuationItemsAction")
        )
        for action in actions:
            for item in action.get("continuationItems", []):
                if action["targetId"] == "comments-section":
                    # Process continuations for comments and replies.
                    continuations[:0] = [
                        ep for ep in search_dict(item, "continuationEndpoint")
                    ]
                if (
                    action["targetId"].startswith("comment-replies-item")
                    and "continuationItemRenderer" in item
                ):
                    # Process the 'Show more replies' button
                    continuations.append(
                        next(search_dict(item, "buttonRenderer"))["command"]
                    )

        for comment in reversed(list(search_dict(response, "commentRenderer"))):
            yield {
                "cid": comment["commentId"],
                "content": "".join(
                    [c["text"] for c in comment["contentText"].get("runs", [])]
                ),
                "time": comment["publishedTimeText"]["runs"][0]["text"],
                "author": comment.get("authorText", {}).get("simpleText", ""),
                "channel": comment["authorEndpoint"]["browseEndpoint"].get(
                    "browseId", ""
                ),
                "likes": int(
                    comment.get("voteCount", {})
                    .get("simpleText", "0")
                    .replace(".", "")
                    .replace("K", "00")
                    .replace("M", "00, 000")
                ),
                "avatar": comment["authorThumbnail"]["thumbnails"][-1]["url"],
                "heart": next(search_dict(comment, "isHearted"), False),
            }

        time.sleep(sleep)
