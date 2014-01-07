#!/usr/bin/python

import pika

#establishes connection to RabbitMQ server as before
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates queue
channel.queue_declare(queue='hello')

#waits for data in a infinite loop and runs callbacks whenever necessary
print ' [*] Waiting for messages. To exit press CTRL+C'

#tells RabbitMQ that this callback function receives messages from the hello queue
channel.basic_consume(callback, queue='hello', no_ack=True)

channel.start_consuming()

#when a message is received, callback is called by the Pika library and prints the contents of the message
def callback(ch, method, properties, body):
        print " [x] Received %r" % (body,)

