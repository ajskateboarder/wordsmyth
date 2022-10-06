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
            executor.submit(ModelStub(_channel).flair, request=Request(texts=v))
            for v in content
        ]
    return as_completed(futures)


def main(texts):
    data = []

    responses = submit_futures(texts)

    for f in responses:
        future = MessageToDict(f.result())
        for item in future["response"]:
            data.append(item)

    return data


if __name__ == "__main__":
    from ast import literal_eval
    from pprint import pprint
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", "-p", action="store_true", help="Format JSON")
    
    pretty = parser.parse_args().pretty
    data = main(literal_eval(list(sys.stdin)[-1]))
    
    if pretty:
        pprint(data)
    else:
        print(json.dumps(data))
    
