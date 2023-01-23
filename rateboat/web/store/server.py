"""gRPC video queue servicer"""

from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Event
from uuid import uuid4
import time

import requests
import grpc

from utils.comments_v3 import download_comments
from algorithms.wrapper import request

from .stubs.queue_pb2_grpc import add_QueueServicer_to_server, QueueServicer
from .stubs.queue_pb2 import QueueStatus


state = []


def send_status(listener, status):
    requests.get(
        f"http://localhost:8081{listener}/send",
        headers={"Status": status},
        timeout=10,
    )


class QueueWorker(Thread):
    def __init__(self, event, video, url):
        Thread.__init__(self)
        self.stopped = event
        self.video = video
        self.url = url

    def run(self):
        s = time.time()
        comments = download_comments(self.video, 10)
        send_status(self.url, "1")
        tmres = request(comments, "torchmoji", count=10)
        send_status(self.url, "1>done")

        send_status(self.url, "2")
        flres = request(comments, "flair")
        send_status(self.url, "2>done")

        comb = [dict(t, **f) for t, f in zip(tmres, flres)]
        send_status(self.url, "0")
        e = time.time()
        print(comb[0], e - s)

        try:
            state.remove(self.video)
        except IndexError:
            pass


def add(video):
    """Add video the global state to indicate that processing is in progress"""
    if video in state:
        return QueueStatus(status="exists", listener=None)
    state.append(video)
    url = f"/queue/{str(uuid4())}"

    thread = QueueWorker(Event(), video, url)
    thread.start()

    return QueueStatus(status="added", listener=url)


class Queue(QueueServicer):
    def check_queue(self, request, _):
        return add(request.video_id)


def main():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_QueueServicer_to_server(Queue(), server)
    server.add_insecure_port("[::]:50056")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
