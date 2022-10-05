#!/home/adijo/Desktop/ytstars/venv/bin/python3

from concurrent.futures import ThreadPoolExecutor, as_completed

from google.protobuf.json_format import MessageToDict
import grpc

from modelparser import Model
from micro.stubs.server_pb2 import Request
from micro.stubs.server_pb2_grpc import ModelStub


channel = grpc.insecure_channel("localhost:50051")


def submit_futures(content):
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(ModelStub(channel).flair, request=Request(texts=v))
            for v in content
        ]
    return as_completed(futures)


def main(texts):
    print("[", end="")

    responses = submit_futures(texts)

    for f in responses:
        future = Model(**MessageToDict(f.result()))
        for item in future.response:
            k = item.sentiment

            print(
                {
                    "text": item.text,
                    "sentiment": k.sentiment,
                    "score": k.score,
                },
                end=",",
            )

        print("]", end="")


if __name__ == "__main__":
    from ast import literal_eval
    import sys

    main(literal_eval(list(sys.stdin)[-1]))
