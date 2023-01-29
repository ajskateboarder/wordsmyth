#!/usr/bin/env python3
"""
Emoji map downloader:
Script to download sentiment information associated
with every emoji used by TorchMoji.
http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html
"""

import json

import requests
from bs4 import BeautifulSoup
from emoji import emojize

REPRS = ":joy: :unamused: :weary: :sob: :heart_eyes: \
:pensive: :ok_hand: :blush: :heart: :smirk: \
:grin: :notes: :flushed: :100: :sleeping: \
:relieved: :relaxed: :raised_hands: :two_hearts: :expressionless: \
:sweat_smile: :pray: :confused: :kissing_heart: :heartbeat: \
:neutral_face: :information_desk_person: :disappointed: :see_no_evil: :tired_face: \
:v: :sunglasses: :rage: :thumbsup: :cry: \
:sleepy: :yum: :triumph: :hand: :mask: \
:clap: :eyes: :gun: :persevere: :smiling_imp: \
:sweat: :broken_heart: :yellow_heart: :musical_note: :speak_no_evil: \
:wink: :skull: :confounded: :smile: :stuck_out_tongue_winking_eye: \
:angry: :no_good: :muscle: :facepunch: :purple_heart: \
:sparkling_heart: :blue_heart: :grimacing: :sparkles:".split(
    " "
)

EMOJIS = list(emojize(emoji, use_aliases=True) for emoji in REPRS)
COMBS = dict(zip(EMOJIS, REPRS))


def main(path: str) -> None:
    req = requests.get(
        "http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html", timeout=20
    )
    soup = BeautifulSoup(req.text, "html.parser")

    trs = soup.find("table").find("tbody").find_all("tr")
    groups = [
        {
            "emoji": td[0].text,
            "repr": COMBS.get(td[0].text, ""),
            "sentiment": list(sent.keys())[
                list(sent.values()).index(max(sent.values()))
            ],
            **sent,
        }
        for tr in trs
        if (td := tr.find_all("td"))
        if (
            sent := {
                "neg": td[5].text,
                "neu": td[6].text,
                "pos": td[7].text,
                "score": td[8].text,
            }
        )
    ]

    extracts = [g for g in groups if any(emoji in g["emoji"] for emoji in EMOJIS)]

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(extracts, fh)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download the Emoji Sentiment Ranking list to a JSON document",
        usage="./tools/emojimap.py ./path/to.json",
    )
    parser.add_argument(dest="path", help="Path to dump emoji data")
    args = parser.parse_args()

    main(args.path)
