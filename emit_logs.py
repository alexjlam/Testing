#!/usr/bin/env python

import pika, sys

#establishes connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates a fanout exchange called logs
channel.exchange_declare(exchange='logs', type='fanout')

#publishes message to exchange
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print " [x] Sent %r" % (message,)
connection.close()
