"""
Matches all the emojis the DeepMoji model uses to descriptions
from the Emoji Sentiment Ranking table
http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html
"""

import requests
from bs4 import BeautifulSoup
from emoji import emojize

EMOJIS = set(
    emojize(emoji, use_aliases=True)
    for emoji in ":joy: :unamused: :weary: :sob: :heart_eyes: \
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
)

print(EMOJIS)

req = requests.get("http://kt.ijs.si/data/Emoji_sentiment_ranking/index.html")
soup = BeautifulSoup(req.text, "html.parser")

trs = soup.find("table").find("tbody").find_all("tr")
groups = [
    {"emoji": td[0].text, "desc": td[-2].text.lower()}
    for tr in trs
    if (td := tr.find_all("td"))
]

for g in groups:
    if any(emoji in g["emoji"] for emoji in EMOJIS):
        print(g)
