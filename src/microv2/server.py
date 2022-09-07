"""Some random docstring"""

from concurrent.futures import ThreadPoolExecutor

import grpc

from microv2.stubs.server_pb2_grpc import add_ModelServicer_to_server, ModelServicer
from microv2.stubs.server_pb2 import Emoji, Emojis, Sentiment, Sentiments, NegNeuPos

from algo.deepmoji import Emojize
from algo.roberta import Roberta


deepmoji = Emojize()
roberta = Roberta()


class Model(ModelServicer):
    def torchmoji(self, request, _):
        response = [
            Emoji(emojis=deepmoji.predict(text), text=text) for text in request.texts
        ]
        return Emojis(response=response)

    def roberta(self, request, _):
        response = [
            Sentiment(sentiment=NegNeuPos(**roberta.predict(text)), text=text)
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
