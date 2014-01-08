#!/usr/bin/env python

import pika

#establishes connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates fanout exchange
channel.exchange_declare(exchange='logs', type='fanout')

#server creates a random, empty queue, and once it disconnects consumer it deletes queue
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

#tells exchange to send message to queue
channel.queue_bind(exchange='logs', queue=queue_name)

#receive needs to wait for emit in order to transfer messages
#therefore run receive first, and then emit in another terminal
print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
        print " [x] %r" % (body,)

#receives messages from callback
channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
