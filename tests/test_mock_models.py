"""Tests for model output generators in `wordsmyth/models/__init__.py`"""
import pytest

from wordsmyth.models import predict_flair, predict_torchmoji


@pytest.mark.usefixtures("mock_torchmoji")
def test_predict_torchmoji(mock_torchmoji):
    """Test the generator variant of TorchMoji prediction with a mock model"""
    output = list(predict_torchmoji(["Hello world!", "Lorem ipsum", "Spam eggs"], 10))
    assert output[0]["emojis"] == mock_torchmoji
    assert output[0]["text"] == "Hello world!"


@pytest.mark.usefixtures("mock_flair")
def test_predict_flair(mock_flair):
    """Test the generator variant of Flair prediction with a mock model"""
    output = list(predict_flair(["Lorem ipsum", "Hello world!", "Spam eggs"]))
    assert output[0]["sentiment"] == mock_flair
    assert output[0]["text"] == "Lorem ipsum"
