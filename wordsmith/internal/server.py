"""gRPC algorithm servicers"""

from concurrent.futures import ThreadPoolExecutor

import grpc

from internal.stubs.server_pb2_grpc import add_ModelServicer_to_server, ModelServicer
from internal.stubs.server_pb2 import Emoji, Emojis, Sentiment, Sentiments, Intensity

from algorithms.deepmoji import Emojize
from algorithms.flairnlp import Flair


deepmoji = Emojize()
flair = Flair()


class Model(ModelServicer):
    def torchmoji(self, request, _):
        response = [
            Emoji(emojis=deepmoji.predict(text, request.count), text=text)
            for text in request.texts
        ]
        return Emojis(response=response)

    def flair(self, request, _):
        response = [
            Sentiment(sentiment=Intensity(**flair.predict(text)), text=text)
            for text in request.texts
        ]
        return Sentiments(response=response)


def main():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_ModelServicer_to_server(Model(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
