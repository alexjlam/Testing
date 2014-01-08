#!/usr/bin/env python

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates a topic exchange
channel.exchange_declare(exchange='topic_logs', type='topic')

#cmd line routing_key for <celerity>.<color>.<animal>
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

#message after routing_key
message = ' '.join(sys.argv[2:]) or 'Hello World'

channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
print " [x] Sent %r:%r" % (routing_key, message)

connection.close()

