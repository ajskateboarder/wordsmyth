"""Tests for model output generators in `wordsmyth/models/__init__.py`"""
from wordsmyth.models import predict_flair
from wordsmyth.models import predict_torchmoji


def test_predict_torchmoji() -> None:
    """Test the generator variant of TorchMoji prediction with a mock model"""
    output = list(predict_torchmoji(["Hello world!", "Lorem ipsum", "Spam eggs"], 10))
    assert output[0]["text"] == "Hello world!"


def test_predict_flair() -> None:
    """Test the generator variant of Flair prediction with a mock model"""
    output = list(predict_flair(["Lorem ipsum", "Hello world!", "Spam eggs"]))

    assert output[0]["text"] == "Lorem ipsum"
    assert output[1]["sentiment"] == "pos"
