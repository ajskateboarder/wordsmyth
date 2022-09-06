import pytest
from grpc._channel import _InactiveRpcError

from microv2.stubs.server_pb2 import Texts


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from microv2.stubs.server_pb2_grpc import add_ModelServicer_to_server

    return add_ModelServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from microv2.server import Model

    return Model()


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    from microv2.stubs.server_pb2_grpc import ModelStub

    return ModelStub(grpc_channel)


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_none(grpc_stub):
    """Test if an empty response returns an empty list as there's nothing to process"""

    request = Texts()
    response = grpc_stub.torchmoji(request)

    assert response.emojis == []


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_exception(grpc_stub):
    """Test if using a non-list type raises an exception"""

    request = texts(texts="Hello world")

    with pytest.raises(_InactiveRpcError) as exc:
        grpc_stub.torchmoji(request)

    error = exc.value.debug_error_string()

    assert "Exception calling application" in error
