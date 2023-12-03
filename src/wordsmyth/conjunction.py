"""Possible thing that may possibly be added"""

from __future__ import annotations

import json

import spacy
from nltk.corpus import sentiwordnet
from numpy import mean

from wordsmyth.constants import DIR_PATH


class Conjunction:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        with open(f"{DIR_PATH}/data/modifiers.json", encoding="utf-8") as fh:
            self.modifiers = {word["word"]: word for word in json.load(fh)}

    @staticmethod
    def _sorted_advmods(items: dict) -> list[dict]:
        """Groups advmods with acomps that are directly next to each other in tokens"""
        grouped = []
        current_group: dict[str, str] = {}
        matched_value = None

        for word, dep in items.items():
            if matched_value == "acomp" and dep == "advmod":
                grouped.append(current_group)
                current_group = {}

            current_group[dep] = word
            matched_value = dep
        if current_group:
            grouped.append(current_group)
        return grouped

    def _word_sentiment(self, text: str, pos: str) -> tuple[str, float]:
        synsets = list(sentiwordnet.senti_synsets(text))
        matched_synsets = [
            s
            for s in synsets
            if s.synset._pos  # pylint: disable=protected-access
            == ("a" if pos in ("ADJ", "acomp") else "r")
        ]

        pos_passes = [e.pos_score() >= 0.625 for e in matched_synsets]
        neg_scores = [1 - e.neg_score() for e in matched_synsets]
        pos_scores = [e.pos_score() for e in matched_synsets]

        return (
            ("pos", mean(pos_scores))
            if pos_passes.count(True) > pos_passes.count(False)
            else ("neg", mean(neg_scores))
        )

    def _pair_sentiment(self, pair: dict[str, str]) -> tuple[str, float]:
        try:
            modifier, initial_adj = pair.items()
        except ValueError:
            modifier, initial_adj = None, list(pair.items())[0]
        adj_sent, adj_score = self._word_sentiment(initial_adj[1], initial_adj[0])
        if modifier:
            if mod := self.modifiers.get(modifier[1]):
                if (
                    adj_sent == "pos"
                    and mod["category"] == "intensifier"
                    and mod["obvious.downtoner"] == "yes"
                ):
                    adj_score *= 2
                if adj_sent == "neg" and mod["category"] == "intensifier":
                    adj_score /= 2
        return (adj_sent, adj_score)

    def detect(self, text: str) -> dict[str, tuple[str, float]]:
        """
        Detect conjugating clauses in a text that possibly impact the true sentiment
        and return a sentiment and an associated intensity
        """
        doc = self.nlp(text)
        cc_tokens = [tok for tok in doc if tok.dep_ == "cc"]

        clause_sent = {}

        for token in cc_tokens:
            mapping = {
                tok.text: tok.dep_
                for tok in token.sent.as_doc()
                if tok.dep_ in ("advmod", "acomp")
            }
            for pair in self._sorted_advmods(mapping):
                phrase = " ".join(pair.values())
                clause_sent[phrase] = self._pair_sentiment(pair)

        return clause_sent
