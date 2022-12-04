"""Backend indexing work which runs in the background"""
import threading
from functools import partial
from collections import deque
import json
import pika

from utils.comments_v3 import download_comments

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost"),
)
channel = connection.channel()

state = deque([])


def add(video):
    """Add video the global state to indicate that processing is in progress"""
    if video in state:
        return {"status": "exists", "state": list(state)}
    state.append(video)
    return {"status": "added", "state": list(state)}


def check_existing(ch, method, props, body):
    """RPC to check if a video is currently in the state"""

    response = add(body.decode())
    if response["status"] == "added":
        ch.basic_publish(
            exchange="",
            routing_key="to_index",
            body=body.decode(),
        )

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def ack_message(inner_channel, delivery_tag):
    if inner_channel.is_open:
        inner_channel.basic_ack(delivery_tag)
    else:
        print("ACK failed")


def passer(inner_channel, method, _, body):
    # TODO: logic goes below vvv
    comments = download_comments("gnupOrSEikQ", 300)
    print("COMMENTS: ", comments[:10])

    cb = partial(ack_message, inner_channel, method.delivery_tag)
    connection.add_callback_threadsafe(cb)
    try:
        state.remove(body.decode())
    except IndexError:
        pass


def callback(inner_channel, method, properties, body):
    t = threading.Thread(
        target=passer,
        args=(
            inner_channel,
            method,
            properties,
            body,
        ),
        daemon=True,
    )
    t.start()


def main():
    """Entrypoint to clean the queues, serve RPCs, and listen for events"""
    channel.queue_delete("rpc_queue")
    channel.queue_delete("to_index")
    channel.queue_declare("rpc_queue")
    channel.queue_declare("to_index")

    channel.basic_consume(queue="rpc_queue", on_message_callback=check_existing)
    channel.basic_consume(queue="to_index", on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()


if __name__ == "__main__":
    main()
