import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import grpc
from google.protobuf.json_format import MessageToDict
from internal.stubs import server_pb2_grpc, server_pb2

channel = grpc.insecure_channel(target="localhost:50051")
stub = server_pb2_grpc.ModelStub(channel=channel)

with open("reviews.json", encoding="utf-8") as fh:
    content = json.load(fh)

stream = open("stream.json", "a+", encoding="utf-8")
stream.write("[")

def torch_iterator(_chunk):
    entry_request = server_pb2.Request(texts=_chunk, count=10)
    yield entry_request

def flair_iterator(_chunk):
    entry_request = server_pb2.Request(texts=_chunk)
    yield entry_request

def create_job(chunk):
    for flair, torch in zip(stub.torchmoji(torch_iterator(chunk)), stub.flair(flair_iterator(chunk))):
        stream.write(f"{json.dumps(dict(MessageToDict(torch), **MessageToDict(flair)))},")

def create_queue():
    futures = []
    with ThreadPoolExecutor() as executor:
        for chunk in content[:1]:
            futures.append(executor.submit(create_job, chunk))

if __name__ == "__main__":
    create_queue()
    stream.write("]")
    stream.close()
