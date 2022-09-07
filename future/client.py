from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

from google.protobuf.json_format import MessageToDict
from youtube_comment_downloader import YoutubeCommentDownloader
import grpc

from microv2.stubs.server_pb2 import Texts
from microv2.stubs.server_pb2_grpc import ModelStub

from parser import Model


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


print("Connecting to gRPC server")

yt = YoutubeCommentDownloader()
channel = grpc.insecure_channel("localhost:50051")

fieldnames = ["text", "sentiment", "neg", "neu", "pos"]


def main(nlps):
    with open("data.csv", "w") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()

        fetch = ModelStub(channel).roberta

        print("Requesting comments")

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch, request=Texts(texts=v)) for v in nlps]

        for f in as_completed(futures):
            future = Model(**MessageToDict(f.result()))
            for sentiment in future.response:
                k = sentiment.sentiment.dict()
                sent = dict(zip(k.values(), k.keys()))[max(list(k.values()))]

                if sent != "neu":
                    writer.writerow(
                        {
                            "text": sentiment.text,
                            "sentiment": sent,
                            "neg": sentiment.sentiment.neg,
                            "neu": sentiment.sentiment.neu,
                            "pos": sentiment.sentiment.pos,
                        }
                    )


main(
    list(
        chunks(
            [
                e["text"]
                for e, _ in zip(yt.get_comments("v9jSFtD40Wk", sort_by=1), range(50))
                if not e["reply"]
            ],
            10,
        )
    )
)
