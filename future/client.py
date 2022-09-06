from concurrent.futures import ThreadPoolExecutor, as_completed

from google.protobuf.json_format import MessageToDict
import grpc

from microv2.stubs.server_pb2 import Texts
from microv2.stubs.server_pb2_grpc import ModelStub

print("Connecting to gRPC server")
channel = grpc.insecure_channel("localhost:50051")


def main(nlps):
    fetch = ModelStub(channel).torchmoji

    print("Requesting comments")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch, request=Texts(texts=v)) for v in nlps]

    for f in as_completed(futures):
        print("Collected")
        print(MessageToDict(f.result()))


main([["This is the shit!", "You are shit."], ["Nice", "Very cool"]])
