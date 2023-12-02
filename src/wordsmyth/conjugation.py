"""Possible thing that may possibly be added"""

from __future__ import annotations

from numpy import mean
import spacy
from nltk.corpus import sentiwordnet


class Conjugation:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")

    def _word_sentiment(self, text: str, pos: str) -> tuple[str, float]:
        synsets = list(sentiwordnet.senti_synsets(text))
        matched_synsets = [
            s
            for s in synsets
            if s.synset._pos  # pylint: disable=protected-access
            == ("a" if pos in ("ADJ", "acomp") else "r")
        ]

        pos_passes = [e.pos_score() >= 0.625 for e in matched_synsets]
        neu_passes = all(
            e.pos_score() <= 0.4 and e.neg_score() <= 0.4 for e in matched_synsets
        )
        neg_scores = [1 - e.neg_score() for e in matched_synsets]
        pos_scores = [e.pos_score() for e in matched_synsets]

        return (
            ("neu", 0.5)
            if neu_passes
            else (
                ("pos", mean(pos_scores))
                if pos_passes.count(True) > pos_passes.count(False)
                else ("neg", mean(neg_scores))
            )
        )

    def _pair_sentiment(self, pair: dict[str, str]):
        try:
            modifier, initial_adj = pair.items()
        except ValueError:
            modifier, initial_adj = None, list(pair.items())[0]
        adj_sent = self._word_sentiment(initial_adj[1], initial_adj[0])
        print(initial_adj[1], adj_sent)
        if modifier:
            mod_sent = self._word_sentiment(modifier[1], modifier[0])
            print(modifier[1], mod_sent)

    @staticmethod
    def _sorted_advmods(items: dict) -> list:
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

    def detect(self, text: str) -> dict[str, list[str]]:
        """Detect conjugating clauses in a text that possibly impact the true sentiment"""
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
                print(self._pair_sentiment(pair))

            clause_sent[token.sent.text] = [
                self._word_sentiment(tok.text, tok.pos_)
                for tok in token.sent.as_doc()
                if tok.dep_ == "acomp"
            ]

        return clause_sent
