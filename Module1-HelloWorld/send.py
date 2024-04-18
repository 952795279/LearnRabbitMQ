#!/usr/bin/env python

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel

# channel.queue_declare(queue="hello")

if __name__ == "__main__":
    print(channel)