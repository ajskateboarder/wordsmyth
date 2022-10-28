#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor, as_completed

from google.protobuf.json_format import MessageToDict
import grpc

from micro.stubs.server_pb2 import Request
from micro.stubs.server_pb2_grpc import ModelStub


_channel = grpc.insecure_channel("localhost:50051")


def submit_futures(content):
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                ModelStub(_channel).torchmoji, request=Request(texts=v, count=10)
            )
            for v in content
        ]
    return as_completed(futures)


def request(texts):
    data = []

    responses = submit_futures(texts)

    for f in responses:
        future = MessageToDict(f.result())
        for item in future["response"]:
            data.append(item)

    return data


def main(stdin):
    from ast import literal_eval
    import json

    stdin = literal_eval(stdin)
    response = request(stdin)

    print(json.dumps(response))


if __name__ == "__main__":
    import sys

    output = list(sys.stdin)[-1]
    print(output)
    main(output)