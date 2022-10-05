"""Test Flair gRPC API"""

import pytest
from grpc._channel import _InactiveRpcError
from google.protobuf.json_format import MessageToDict

from micro.stubs.server_pb2 import Request
from .classes import Flair


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_none(grpc_stub):
    """Test if an empty response returns an empty list as there's nothing to process"""

    request = Request()
    response = MessageToDict(grpc_stub.flair(request))

    assert response == {}


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_some(grpc_stub, capsys):
    """Test some sample texts"""

    request = Request(texts=["This sucks!", "Nice tutorial"])
    response = MessageToDict(grpc_stub.flair(request))

    assert response["response"]

    try:
        objs = [Flair(**item) for item in response["response"]]
    except Exception as exc:
        raise Exception(exc) from exc

    assert len(objs) == 2
    assert objs[0].sentiment == "neg"
    assert objs[1].sentiment == "pos"


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_exception(grpc_stub):
    """Test if using a non-list type raises an exception"""

    request = Request(texts="Hello world")

    with pytest.raises(_InactiveRpcError) as exc:
        grpc_stub.flair(request)

    error = exc.value.debug_error_string()

    assert "Exception calling application" in error
