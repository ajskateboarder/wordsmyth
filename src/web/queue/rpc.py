"""
RPC Client to check the state of video processing on the server
Most of this code is boilerplate from the RabbitMQ docs XD
"""
import uuid
import pika
import json


class VideoProcessingState:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "localhost",
            )
        )

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(body),
        )
        self.connection.process_data_events(time_limit=None)
        return self.response
