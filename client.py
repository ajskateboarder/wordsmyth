import time
import random

import grpc
from google.protobuf.json_format import MessageToDict

from internal.stubs import server_pb2_grpc, server_pb2

channel = grpc.insecure_channel(target="localhost:50051")
stub = server_pb2_grpc.ModelStub(channel=channel)
text = ["LOL", "YES", "BAD"]


def entry_request_iterator():
    for _ in range(1, 5):
        entry_request = server_pb2.Request(texts=text)
        yield entry_request
        time.sleep(1)
        random.shuffle(text)


for entry_response in stub.torchmoji(entry_request_iterator()):
    print(MessageToDict(entry_response))
