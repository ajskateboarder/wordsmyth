"""Fixtures for mocked Flair and TorchMoji"""
from __future__ import annotations
from typing import Any

from pytest_mock import MockerFixture
import pytest

from wordsmyth.models.flair import Flair
from wordsmyth.models.torchmoji import TorchMoji

MOCK_EMOJIS = [
    ":skull:",
    ":sparkling_heart:",
    ":neutral_face:",
    ":confused:",
    ":angry:",
    ":joy:",
    ":unamused:",
    ":blush:",
    ":broken_heart:",
    ":ok_hand:",
]


@pytest.fixture
def mock_flair(mocker: MockerFixture) -> dict[str, Any]:
    """A mocked version of Flair which returns a fixed sentiment output"""

    def _mock_prediction(self, text=None):
        return {"sentiment": "pos", "score": 0.907334}

    mocker.patch.object(Flair, "__init__", lambda self: None)
    mocker.patch.object(Flair, "predict", _mock_prediction)
    return {"sentiment": "pos", "score": 0.907334}


@pytest.fixture
def mock_torchmoji(mocker: MockerFixture) -> list[str]:
    """A mocked version of TorchMoji which returns a fixed emoji output"""

    def _mock_prediction(self, text=None, top_n=None):
        return MOCK_EMOJIS

    mocker.patch.object(TorchMoji, "__init__", lambda self: None)
    mocker.patch.object(TorchMoji, "predict", _mock_prediction)
    return MOCK_EMOJIS
