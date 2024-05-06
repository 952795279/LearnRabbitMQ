#! /usr/bin/env python

import pika
import sys
import time
import os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # 声明队列
    channel.queue_declare("hello")

    # 定义回调函数
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b"."))
        print(" [x] Done")

    channel.basic_consume("hello", auto_ack=True, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)