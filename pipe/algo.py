#!/usr/bin/env python3
# pylint: disable=import-outside-toplevel

from concurrent.futures import ThreadPoolExecutor, as_completed

from google.protobuf.json_format import MessageToDict
import grpc

from micro.stubs.server_pb2 import Request
from micro.stubs.server_pb2_grpc import ModelStub


_channel = grpc.insecure_channel("localhost:50051")


def request(texts, api, **args):
    data = []

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(ModelStub(_channel).__dict__[api], request=Request(texts=v, **args))
            for v in texts
        ]

    responses = as_completed(futures)
    for f in responses:
        future = MessageToDict(f.result())
        for item in future["response"]:
            data.append(item)

    return data


def main(flair, torch, comments):
    tmres = request(comments, "torchmoji") if torch else None
    flres = request(comments, "flair") if flair else None

    if tmres and flres:
        print(json.dumps([dict(t, **f) for t, f in zip(tmres, flres)]))
    else:
        if tmres:
            print(json.dumps(tmres))
        if flres:
            print(json.dumps(flres))


if __name__ == "__main__":
    from ast import literal_eval
    import argparse
    import sys
    import json

    parser = argparse.ArgumentParser(
        description="Pass comment data to Flair and/or TorchMoji for easy data pipelining",
        usage="./tools/comments.py <youtube video id> <number of comments> | ./algo.py -tf"
    )
    parser.add_argument("--torch", "-t", help="Pass data to TorchMoji", action="store_true")
    parser.add_argument("--flair", "-f", help="Pass data to Flair", action="store_true")
    args = parser.parse_args()

    stdin = list(sys.stdin)[1]
    stdin = literal_eval(stdin)

    main(args.flair, args.torch, stdin)