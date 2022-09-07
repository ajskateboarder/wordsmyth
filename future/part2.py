from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.protobuf.json_format import MessageToDict
import pandas as pd
import grpc

from microv2.stubs.server_pb2 import Texts
from microv2.stubs.server_pb2_grpc import ModelStub


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


print("Connecting to gRPC server")
channel = grpc.insecure_channel("localhost:50051")


def main():
    df = pd.read_csv("./future/data.csv")
    text = list(chunks(df["text"].to_list(), 5))

    fetch = ModelStub(channel).torchmoji

    print("Requesting comments")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch, request=Texts(texts=v)) for v in text]

    emojis = []
    for f in as_completed(futures):
        future = MessageToDict(f.result())
        for res in future["response"]:
            emojis.append(", ".join(res["emojis"]))

    df["emojis"] = emojis
    print(
        df.to_csv(
            "./extracts.csv", columns=["text", "sentiment", "pos", "neg", "emojis"]
        )
    )


main()
