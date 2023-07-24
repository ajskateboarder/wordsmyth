"""
Video indexer/comment downloader
Bulk-request comments and dump them to a JSON file
"""
from __future__ import annotations

from typing import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote_plus
import json
import re

import requests
from youtube_comment_downloader import YoutubeCommentDownloader


class YouTubeScraper:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.yt_session = YoutubeCommentDownloader()

    def get_query(self, search: str) -> list[str]:
        """Fetch video IDs from a search result page"""
        page = self.session.get(
            f"https://www.youtube.com/results?search_query={quote_plus(search)}"
        ).text
        return list(set(re.findall(r"/watch\?v=(\S{11})", page)))

    def get_home(self) -> list[str]:
        page = self.session.get("https://www.youtube.com").text
        return list(set(re.findall(r"/watch\?v=(\S{11})", page)))

    def _fetch_comments(self, video_id: str, limit: int) -> Generator[dict, None, None]:
        for comment_, _ in zip(
            self.yt_session.get_comments(video_id, sort_by=1), range(limit + 1)
        ):
            if not comment_["reply"]:
                yield {"commentText": comment_["text"], "videoId": video_id}

    def fetch_comments(self) -> Generator[Generator[dict, None, None], None, None]:
        items = self.get_home()[:10]
        with ThreadPoolExecutor(max_workers=len(items)) as executor:
            futures = [
                executor.submit(self._fetch_comments, video, 50) for video in items
            ]
            for future in as_completed(futures):
                yield future.result()


# TODO: Formal CLI interface
for video in YouTubeScraper().fetch_comments():
    for review in video:
        print(json.dumps(review))
