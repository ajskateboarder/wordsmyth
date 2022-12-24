def ack_message(inner_channel, delivery_tag):
    if inner_channel.is_open:
        inner_channel.basic_ack(delivery_tag)
    else:
        print("ACK failed")
