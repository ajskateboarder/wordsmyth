import json

import numpy as np
from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from emoji import emojize

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
:sparkling_heart: :blue_heart: :grimacing: :sparkles:".split(' ')

vocab_file_path = 'src/deepmoji/model/vocabulary.json'
model_weights_path = 'src/deepmoji/model/pytorch_model.bin'

def top_elements(array, k):
        ind = np.argpartition(array, -k)[-k:]
        return ind[np.argsort(array[ind])][::-1]

class Emojize:
    def __init__(self):
        with open(vocab_file_path, 'r') as f:
            vocabulary = json.load(f)

        max_sentence_length = 100
        self.st = SentenceTokenizer(vocabulary, max_sentence_length)
        self.model = torchmoji_emojis(model_weights_path)

    def predict(self, text):
        if not isinstance(text, list):
            text = [text]

        tokenized, _, _ = self.st.tokenize_sentences(text)
        prob = self.model(tokenized)[0]

        emoji_ids = top_elements(prob, 1)
        emojis = list(map(lambda x: EMOJIS[x], emoji_ids))
        
        return emojize(emojis[0], use_aliases=True)