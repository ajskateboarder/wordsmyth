"""ok"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import grpc

from microv2.server_pb2 import sentiments, texts
from microv2.server_pb2_grpc import ModelStub

print("Connecting to gRPC server")
channel = grpc.insecure_channel("localhost:50051")


def main(nlps):
    fetch = ModelStub(channel).roberta

    print("Requesting comments")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch, texts(texts=v)) for v in nlps]

    for f in as_completed(futures):
        print("Collected")
        print([[float(g) for g in e.split(", ")] for e in f.result().sentiments])


main([["This is the shit!", "You are shit."], ["Nice", "Very cool"]])
