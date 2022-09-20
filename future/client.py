from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

from google.protobuf.json_format import MessageToDict
from youtube_comment_downloader import YoutubeCommentDownloader
import grpc

from .modelparser import Model
from micro.stubs.server_pb2 import Request
from micro.stubs.server_pb2_grpc import ModelStub


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


print("Connecting to gRPC server")

yt = YoutubeCommentDownloader()
channel = grpc.insecure_channel("localhost:50051")

fieldnames = ["text", "sentiment", "score"]


def main(nlps):
    with open("data.csv", "w") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()

        fetch = ModelStub(channel).flair

        print("Requesting comments")

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch, request=Request(texts=v)) for v in nlps]

        for f in as_completed(futures):
            print(f.result())
            future = Model(**MessageToDict(f.result()))
            for sentiment in future.response:
                k = sentiment.sentiment

                writer.writerow(
                    {
                        "text": sentiment.text,
                        "sentiment": k.sentiment,
                        "score": k.score,
                    }
                )


main(
    list(
        chunks(
            [
                e["text"]
                for e, _ in zip(yt.get_comments("GZvSYJDk-us", sort_by=1), range(300))
                if not e["reply"]
            ],
            30,
        )
    )
)
