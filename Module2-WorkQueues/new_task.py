#! /usr/bin/env python

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# 声明队列
channel.queue_declare(queue="hello")

# 指定交换机和队列名称
message = " ".join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='', routing_key="hello", body=message)

print(f" [x] Sent {message}")
connection.close()