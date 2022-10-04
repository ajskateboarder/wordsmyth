#!/usr/bin/env python3
"""
Comment downloader:
Script to bulk request comments and dump them to a JSON file as chunks
"""

import sys
import json

from youtube_comment_downloader import YoutubeCommentDownloader

_yt = YoutubeCommentDownloader()


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def download_comments(video_id, limit):
    comments = []
    chunk = []

    for e, (c, _) in enumerate(
        zip(_yt.get_comments(video_id, sort_by=1), range(limit + 1))
    ):
        sys.stdout.write(f"{e} comments\r")
        sys.stdout.flush()

        if len(chunk) == limit / 10:
            comments.append(chunk)
            chunk = []
        else:
            chunk.append(c["text"])

    sys.stdout.write("\n\r")
    sys.stdout.flush()

    return comments


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download a specific number of comments in chunks to a JSON document",
        usage="./tools/dlcent.py ./path/to.json <youtube video id> <number of comments>"
    )
    parser.add_argument(dest="path", help="Path to dump comments")
    parser.add_argument(dest="video_id", help="YouTube video ID")
    parser.add_argument(dest="limit", help="Number of comments to download", type=int)
    args = parser.parse_args()

    comments = download_comments(args.video_id, args.limit)

    # GZvSYJDk-us

    with open(args.path, "w", encoding="utf-8") as fh:
        json.dump(comments, fh)
