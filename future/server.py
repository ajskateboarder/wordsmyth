"""Backend indexing work which runs in the background"""
import pika
import threading
from functools import partial
import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "localhost",
        5672,
        "rabbit",
        credentials=pika.PlainCredentials("user", "password"),
    ),
)
channel = connection.channel()

state = []


def add(n):
    """Add video the global state to indicate that processing is in progress"""
    if n in state:
        return "exists"
    state.append(n)
    return "added"


def check_existing(ch, method, props, body):
    """RPC to check if a video is currently in the state"""

    print(f" [.] add({body})")
    response = add(body.decode())
    if response == "added":
        ch.basic_publish(
            exchange="",
            routing_key="to_index",
            body=body.decode(),
        )

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def ack_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        print("ACK failed")


def passer(channel, method, properties, body):
    time.sleep(2)
    cb = partial(ack_message, channel, method.delivery_tag)
    connection.add_callback_threadsafe(cb)
    try:
        state.remove(body.decode())
    except IndexError:
        pass
    print(body, state)


def callback(channel, method, properties, body):
    t = threading.Thread(
        target=passer,
        args=(
            channel,
            method,
            properties,
            body,
        ),
        daemon=True,
    )
    t.start()


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
