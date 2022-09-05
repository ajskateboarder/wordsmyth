"""Some random docstring"""

from concurrent.futures import ThreadPoolExecutor
import logging

import grpc

from microv2.server_pb2_grpc import ModelServicer, add_ModelServicer_to_server
from microv2.server_pb2 import emojis, sentiments


from algo.deepmoji import Emojize
from algo.roberta import Roberta

e = Emojize()
r = Roberta()


class Model(ModelServicer):
    def torchmoji(self, request, _):
        response = [", ".join(e.predict(text)) for text in request.texts]
        return emojis(emojis=response)

    def roberta(self, request, _):
        response = [
            str(r.predict(text)).replace("[", "").replace("]", "")
            for text in request.texts
        ]
        return sentiments(sentiments=response)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_ModelServicer_to_server(Model(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
