"""Test Torchmoji gRPC API"""

import pytest
from grpc._channel import _InactiveRpcError
from google.protobuf.json_format import MessageToDict

from interns.stubs.server_pb2 import Request
from .classes import Torch


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_none(grpc_stub):
    """Test if an empty response returns an empty list as there's nothing to process"""

    request = Request()
    response = MessageToDict(grpc_stub.torchmoji(request))

    assert response == {}


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_some(grpc_stub, capsys):
    """Test some sample texts and validate each response with a model"""

    request = Request(texts=["This isn't too bad!", "Nice tutorial"], count=2)
    response = MessageToDict(grpc_stub.torchmoji(request))

    assert response["response"]
    for item in response["response"]:
        try:
            obj = Torch(**item)
            assert len(obj.emojis) == 2
        except Exception as exc:
            raise Exception(exc) from exc


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_exception(grpc_stub):
    """Test if using a non-list type raises an RPC server exception"""

    request = Request(texts="Hello world")

    with pytest.raises(_InactiveRpcError) as exc:
        grpc_stub.torchmoji(request)

    error = exc.value.debug_error_string()
    assert "Exception calling application" in error
