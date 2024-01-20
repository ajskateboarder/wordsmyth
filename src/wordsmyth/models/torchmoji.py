"""
Abstracted library to make emoji processing nicer, mostly from this gist
https://gist.github.com/cw75/57ca89cfa496f10c7c7b888ec5703d7f#file-emojize-py
"""
from __future__ import annotations

import json

import numpy as np
from torchmoji.model_def import torchmoji_emojis
from torchmoji.sentence_tokenizer import SentenceTokenizer

from wordsmyth.constants import DIR_PATH

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

VOCAB_FILE_PATH = f"{DIR_PATH}/data/vocabulary.json"
MODEL_WEIGHTS_PATH = f"{DIR_PATH}/data/pytorch_model.bin"


def top_elements(array: np.ndarray, k: int) -> np.ndarray:
    """Select maximum elements from Numpy array"""
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]


class TorchMoji:
    """Abstracted TorchMoji model"""

    def __init__(self) -> None:
        with open(VOCAB_FILE_PATH, encoding="utf-8") as fh:
            vocabulary = json.load(fh)

        max_sentence_length = 100
        self.tokenizer = SentenceTokenizer(vocabulary, max_sentence_length)
        self.model = torchmoji_emojis(MODEL_WEIGHTS_PATH, return_attention=True)

    def predict(self, text: str | list, top_n: int = 5) -> list[str]:
        """Emoji prediction"""

        if not isinstance(text, list):
            text = [text]

        probabilities, _ = self.model(self.tokenizer.tokenize_sentences(text)[0])

        emoji_ids = top_elements(probabilities[0], top_n)
        emojis = list(map(lambda x: EMOJIS[x], emoji_ids))

        return emojis
