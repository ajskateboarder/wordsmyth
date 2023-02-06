#!/usr/bin/env python3

from ast import literal_eval
from typing import List, Dict, Any, Union
import argparse
import sys
import json

from concurrent.futures import ThreadPoolExecutor, as_completed

from google.protobuf.json_format import MessageToDict
import grpc

from internal.stubs.server_pb2 import Request
from internal.stubs.server_pb2_grpc import ModelStub


_channel = grpc.insecure_channel("localhost:50051")


def dump_csv(data: List[Dict[str, Any]]) -> str:
    """Simple wrapper around generating csv from JSON"""
    import pandas as pd

    df = pd.DataFrame()

    df["sentiment"] = [m["sentiment"]["sentiment"] for m in data]
    df["score"] = [m["sentiment"]["score"] for m in data]
    df["text"] = [m["text"] for m in data]
    df["emojis"] = [",".join(m["emojis"]) for m in data]

    return df.to_csv()


def request(texts: List[List[str]], api: str, **params: int) -> List[Dict[str, Any]]:
    """Make parallel requests to a gRPC api"""
    data: List[Dict[str, str]] = []

    with ThreadPoolExecutor() as executor:
        futures = []
        for v in texts:
            futures.append(executor.submit(
                ModelStub(_channel).__dict__[api],
                request=Request(
                    texts=[e.encode("utf-8", "ignore") for e in v], **params
                ),
            ))

    responses = as_completed(futures)
    for f in responses:
        future = MessageToDict(f.result())
        for item in future["response"]:
            data.append(item)

    return data


def main(
    flair: bool,
    torch: bool,
    csv: bool,
    comments: List[List[str]],
) -> None:
    """Fetch algorithm responses and dump data as JSON"""
    tmres = request(comments, "torchmoji", count=10) if torch else None
    flres = request(comments, "flair") if flair else None

    if tmres and flres:
        comb = [dict(t, **f) for t, f in zip(tmres, flres)]
        print(dump_csv(comb) if csv else json.dumps(comb))
    elif tmres:
        print(dump_csv(tmres) if csv else json.dumps(tmres))
    elif flres:
        print(dump_csv(flres) if csv else json.dumps(flres))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pass comment data to Flair and/or TorchMoji for easy data pipelining",
        usage="./tools/comments.py <youtube video id> <number of comments> | ./algo.py -tf",
    )
    parser.add_argument(
        "--torch", "-t", help="Pass data to TorchMoji", action="store_true"
    )
    parser.add_argument("--flair", "-f", help="Pass data to Flair", action="store_true")
    parser.add_argument("--csv", help="Convert output to CSV", action="store_true")

    args = parser.parse_args()

    stdin: Union[List[str], str] = list(sys.stdin)
    try:
        stdin = stdin[1]
    except IndexError:
        stdin = stdin[0]
    stdin = literal_eval(stdin)

    main(args.flair, args.torch, args.csv, stdin)  # type: ignore
