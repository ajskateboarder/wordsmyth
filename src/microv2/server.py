"""Some random docstring"""

from concurrent.futures import ThreadPoolExecutor

import grpc

<<<<<<< HEAD
from microv2.stubs.server_pb2_grpc import add_ModelServicer_to_server, ModelServicer
from microv2.stubs.server_pb2 import Emoji, Emojis, Sentiment, Sentiments
=======
from microv2.server_pb2_grpc import ModelServicer, add_ModelServicer_to_server
from microv2.server_pb2 import emojis, sentiments

>>>>>>> db68cdb87ca9b53b9071dbc82dd375f9d7bbcbb1

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
<<<<<<< HEAD
            Sentiment(**roberta.predict(text), text=text) for text in request.texts
        ]
        return Sentiments(response=response)
=======
            str(r.predict(text)).replace("[", "").replace("]", "")
            for text in request.texts
        ]
        return sentiments(sentiments=response)
>>>>>>> db68cdb87ca9b53b9071dbc82dd375f9d7bbcbb1


def main():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_ModelServicer_to_server(Model(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
