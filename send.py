#!/usr/bin/python

import pika

#establishes connection with RabbitMQ server to a broker on the local machine
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates queue to where the message will be delivered, queue is called 'hello'
channel.queue_declare(queue='hello')

#message goes through exchange before going to the queue
#default exchange is an empty string, this allows us to specify exactly which queue the message goes to
#queue name is specified in routing_key
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print " [x] Sent 'Hello World!'"

#closes the connection
connection.close()
