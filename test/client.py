"""ok"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import grpc

from server_pb2 import query
from server_pb2_grpc import YoutubeCommentsStub

print("Connecting to gRPC server")
channel = grpc.insecure_channel("localhost:50051")


def main(video_ids):
    fetch = YoutubeCommentsStub(channel).fetch

    print("Requesting comments")

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch, query(videoId=v, limit=200)) for v in video_ids
        ]

    for f in as_completed(futures):
        print("Collected")


main(["v9jSFtD40Wk", "QGlCjVG-Hyc"])
