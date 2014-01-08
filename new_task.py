#!/usr/bin/python

import pika
import sys

#sends some message from the command line or "Hello World!"
message = ' '.join(sysargv[1:]) or "Hello World!"

#establishes connection with RabbitMQ server to a broker on the local machine
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates queue to where the message will be delivered, queue is called 'task_queue'
#queue is made "durable" so as to not lose queue or message if RabbitMQ crashes
channel.queue_declare(queue='task_queue', durable=True)

#message goes through exchange before going to the queue
#default exchange is an empty string, this allows us to specify exactly which queue the message goes to
#queue name is specified in routing_key
channel.basic_publish(exchange='', routing_key='hello', body=message)
#also set routing_key to task_queue for durability, and marks message as persistent
channel.basic_publish(exchange='', routing_key='task_queue', body=message, propertires=pika.BasicProperties(delivery_mode=2))
print " [x] Sent %r" % (message,)

#closes the connection
connection.close()
