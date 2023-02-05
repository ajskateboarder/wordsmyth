#!/usr/bin/env python3

"""
Comment downloader:
Script to bulk request comments and dump them to a JSON file as chunks
"""
# NOTE: Move to a scripts folder

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
        sys.stderr.write(f"{e} comments\r")
        sys.stderr.flush()

        if len(chunk) == int(limit / 10):
            comments.append(chunk)
            chunk = []
        else:
            if not c["reply"]:
                chunk.append(c["text"])

    sys.stdout.write("\n\r")
    sys.stdout.flush()
    sys.stdout.flush()

    return comments


def main(video_id, limit):
    # GZvSYJDk-us
    comments = download_comments(video_id, limit)

    print(json.dumps(comments), end="")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download a specific number of comments in chunks to a JSON document",
        usage="./tools/comments.py <youtube video id> <number of comments>",
    )
    parser.add_argument(dest="video_id", help="YouTube video ID")
    parser.add_argument(dest="limit", help="Number of comments to download", type=int)
    args = parser.parse_args()

    main(args.video_id, args.limit)
