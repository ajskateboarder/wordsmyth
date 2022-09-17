import pytest
from grpc._channel import _InactiveRpcError
from google.protobuf.json_format import MessageToDict

from micro.stubs.server_pb2 import Request


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from micro.stubs.server_pb2_grpc import add_ModelServicer_to_server

    return add_ModelServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from micro.server import Model

    return Model()


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    from micro.stubs.server_pb2_grpc import ModelStub

    return ModelStub(grpc_channel)


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_none(grpc_stub):
    """Test if an empty response returns an empty list as there's nothing to process"""

    request = Request()
    response = MessageToDict(grpc_stub.torchmoji(request))

    assert response == {}


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_some(grpc_stub, capsys):
    """Test some sample texts"""

    request = Request(texts=["This isn't too bad!", "Nice tutorial"])
    response = MessageToDict(grpc_stub.torchmoji(request))

    with capsys.disabled():
        print(response)

    assert True


@pytest.mark.filterwarnings("ignore::UserWarning", "ignore::DeprecationWarning")
def test_exception(grpc_stub):
    """Test if using a non-list type raises an exception"""

    request = Request(texts="Hello world")

    with pytest.raises(_InactiveRpcError) as exc:
        grpc_stub.torchmoji(request)

    error = exc.value.debug_error_string()

    assert "Exception calling application" in error
