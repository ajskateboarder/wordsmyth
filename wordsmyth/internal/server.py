"""gRPC algorithm servicer"""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Iterator

import grpc

from internal.stubs.server_pb2_grpc import add_ModelServicer_to_server, ModelServicer
from internal.stubs.server_pb2 import (
    Emoji,
    Sentiment,
    Intensity,
    Request,
)

from algorithms.deepmoji import Emojize
from algorithms.flairnlp import Flair


deepmoji = Emojize()
flair = Flair()


class Model(ModelServicer):
    """Runs the algorithms as gRPC methods"""

    def torchmoji(self, request_iterator: Request, _: Any) -> Iterator[Emoji]:
        for request in request_iterator:
            for text in request.texts:
                print(f"Completing: {text}")
                yield Emoji(
                    emojis=deepmoji.predict(text, request.count),
                    text=text,
                )

    def flair(self, request_iterator: Request, _: Any) -> Sentiment:
        for request in request_iterator:
            for text in request.texts:
                print(f"Completing: {text}")
                yield Sentiment(sentiment=Intensity(**flair.predict(text)), text=text)


def main() -> None:
    """Server entrypoint"""

    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_ModelServicer_to_server(Model(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
