#!/usr/bin/env python3

from ast import literal_eval
from typing import List, Dict, Any
import argparse
import sys
import json

from concurrent.futures import ThreadPoolExecutor, as_completed

from google.protobuf.json_format import MessageToDict
import pandas as pd
import grpc

from micro.stubs.server_pb2 import Request
from micro.stubs.server_pb2_grpc import ModelStub


_channel = grpc.insecure_channel("localhost:50051")


def dump_csv(data: List[Dict[str, Any]]):
    """Simple wrapper around generating csv from JSON"""
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
        futures = [
            executor.submit(
                ModelStub(_channel).__dict__[api],
                request=Request(
                    texts=[t.encode("utf-8", "replace").decode("utf-8") for t in v],
                    **params
                ),
            )
            for v in texts
        ]

    responses = as_completed(futures)
    for f in responses:
        future = MessageToDict(f.result())
        for item in future["response"]:
            data.append(item)

    return data


def main(flair: bool, torch: bool, csv: bool, comments: "list[list[str]]"):
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

    stdin = list(sys.stdin)[1]
    stdin = literal_eval(stdin)

    main(args.flair, args.torch, args.csv, stdin)
