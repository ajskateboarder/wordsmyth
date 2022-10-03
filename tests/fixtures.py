from pytest import fixture


@fixture(scope="module")
def grpc_add_to_server():
    from micro.stubs.server_pb2_grpc import add_ModelServicer_to_server

    return add_ModelServicer_to_server


@fixture(scope="module")
def grpc_servicer():
    from micro.server import Model

    return Model()


@fixture(scope="module")
def grpc_stub(grpc_channel):
    from micro.stubs.server_pb2_grpc import ModelStub

    return ModelStub(grpc_channel)
