"""Possible thing that may possibly be added"""

from __future__ import annotations

import spacy
from spacy import displacy
from nltk.corpus import sentiwordnet


class ConjugationDetection:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")

    def _get_word_sentiment(self, text: str, pos: str) -> str:
        synsets = list(sentiwordnet.senti_synsets(text))
        pos_synsets = [
            s.obj_score() > 0.625
            for s in synsets
            if synsets[0].synset._pos  # pylint: disable=protected-access
            == pos[0].lower()
        ]
        return "pos" if pos_synsets.count(True) > pos_synsets.count(False) else "neg"

    def detect(self, text: str) -> dict[str, list[str]]:
        """Detect conjugating clauses in a text that possibly impact the true sentiment"""
        doc = self.nlp(text)
        cc_tokens = [tok for tok in doc if tok.dep_ == "cc"]
        print(cc_tokens)

        clause_sent = {}

        for token in cc_tokens:
            clause_sent[token.sent.text] = [
                self._get_word_sentiment(tok.text, tok.pos_)
                for tok in token.sent.as_doc()
                if tok.dep_ == "acomp"
            ]

        return clause_sent

    def display(self, text: str) -> None:
        displacy.serve(self.nlp(text))


if __name__ == "__main__":
    detector = ConjugationDetection()
    text = "It has good quality but it's battery life is short."
    print(detector.detect(text))
    detector.display(text)
