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
            executor.submit(ModelStub(_channel).torchmoji, request=Request(texts=v))
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


def main(pretty, stdin):
    from pprint import pprint
    from helpers import convert_stdin
    import json

    stdin = convert_stdin(stdin)
    response = request(stdin)

    if pretty:
        pprint(response)
    else:
        print(json.dumps(response))


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", "-p", action="store_true", help="Format JSON")

    args = parser.parse_args()
    output = list(sys.stdin)[-1]
    main(args.pretty, output)
