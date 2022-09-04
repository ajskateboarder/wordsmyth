"""Some random docstring"""

from concurrent.futures import ThreadPoolExecutor
import logging
import json

import grpc
from youtube_comment_downloader import YoutubeCommentDownloader

from server_pb2_grpc import (
    YoutubeCommentsServicer,
    add_YoutubeCommentsServicer_to_server,
)
from server_pb2 import comments


com = YoutubeCommentDownloader()


class YoutubeComments(YoutubeCommentsServicer):
    def fetch(self, request, _):
        gen = com.get_comments("QGlCjVG-Hyc", sort_by=1)
        response = [json.dumps(g[0]) for g in zip(gen, range(request.limit))]

        return comments(comments=response)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_YoutubeCommentsServicer_to_server(YoutubeComments(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
