"""
Abstracted library to make emoji processing nicer, mostly from this gist
https://gist.github.com/cw75/57ca89cfa496f10c7c7b888ec5703d7f#file-emojize-py
"""

import json
from typing import List, Union

import numpy as np
from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis

EMOJIS = ":joy: :unamused: :weary: :sob: :heart_eyes: \
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

VOCAB_FILE_PATH = "./algorithms/vocabulary.json"
MODEL_WEIGHTS_PATH = "./algorithms/pytorch_model.bin"


def top_elements(array: np.ndarray, k: int) -> np.ndarray:
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]


class TorchMoji:
    def __init__(self) -> None:
        with open(VOCAB_FILE_PATH, encoding="utf-8") as fh:
            vocabulary = json.load(fh)

        max_sentence_length = 100
        self.st = SentenceTokenizer(vocabulary, max_sentence_length)
        self.model = torchmoji_emojis(MODEL_WEIGHTS_PATH)

    def predict(self, text: Union[str, list], top_n: int = 5) -> List[str]:
        """Emoji prediction"""

        if not isinstance(text, list):
            text = [text]

        tokenized, _, _ = self.st.tokenize_sentences(text)
        prob = self.model(tokenized)[0]

        emoji_ids = top_elements(prob, top_n)
        emojis = list(map(lambda x: EMOJIS[x], emoji_ids))

        return emojis
