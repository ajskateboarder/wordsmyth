#!/usr/bin/env python3

from __future__ import annotations
from ast import literal_eval
from typing import Any, Generator
import argparse
import sys
import json

from google.protobuf.json_format import MessageToDict
import pandas as pd
import grpc

from internal.stubs.server_pb2 import Request
from internal.stubs.server_pb2_grpc import ModelStub


class AlgorithmWrapper:
    """Algorithm gRPC client as a class-based API"""

    def __init__(self, url: str = "localhost:50051") -> None:
        _channel = grpc.insecure_channel(url)
        self._stub = ModelStub(channel=_channel)

    @staticmethod
    def _flair_iterator(text: list[list[str]]) -> Generator[Request, None, None]:
        for chunk in text:
            entry_request = Request(texts=chunk)
            yield entry_request

    @staticmethod
    def _torch_iterator(
        text: list[list[str]], count: int
    ) -> Generator[Request, None, None]:
        for chunk in text:
            entry_request = Request(texts=chunk, count=count)
            yield entry_request

    def request(
        self, text: list[list[str]], emojis: int
    ) -> Generator[dict[str, Any], None, None]:
        """Request both Flair and TorchMoji with multiple chunks of text"""

        for (
            flair,
            torch,
        ) in zip(self.flair(text), self.torch(text, emojis)):
            yield dict(torch, **flair)

    def flair(self, text: list[list[str]]) -> Generator[dict[str, Any], None, None]:
        """Request the Flair service with multiple chunks of text"""

        for flair in self._stub.flair(self._flair_iterator(text)):
            yield MessageToDict(flair)

    def torch(
        self, text: list[list[str]], emojis: int
    ) -> Generator[dict[str, Any], None, None]:
        """Request the TorchMoji service with multiple chunks of text"""

        for torch in self._stub.torchmoji(self._torch_iterator(text, emojis)):
            yield MessageToDict(torch)


def dump_csv(data: "list[dict[str, Any]]") -> pd.DataFrame:
    """Simple wrapper around generating csv from JSON"""
    import pandas as pd

    df = pd.DataFrame()

    df["sentiment"] = [m["sentiment"]["sentiment"] for m in data]
    df["score"] = [m["sentiment"]["score"] for m in data]
    df["text"] = [m["text"] for m in data]
    df["emojis"] = [",".join(m["emojis"]) for m in data]

    return df.to_csv()


def request(texts: list[list[str]], api: str, **params: int) -> "list[dict[str, Any]]":
    """Make parallel requests to a gRPC api"""
    data = []

    with ThreadPoolExecutor() as executor:
        futures = []
        for v in texts:
            futures.append(
                executor.submit(
                    ModelStub(_channel).__dict__[api],
                    request=Request(
                        texts=[e.encode("utf-8", "ignore") for e in v], **params
                    ),
                )
            )

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
    comments: list[list[str]],
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

    stdin: "list[str] | str" = list(sys.stdin)
    try:
        stdin = stdin[1]
    except IndexError:
        stdin = stdin[0]
    stdin = literal_eval(stdin)

    main(args.flair, args.torch, args.csv, stdin)  # type: ignore
