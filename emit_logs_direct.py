#!/usr/bin/env python

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#create direct exchange to send directly to queue(s)
channel.exchange_declare(exchange='direct_logs', type='direct')

#severity is the first cmd line arg or 'info'
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

#ready to send a message with severity being 'info', 'warning', or 'error'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
print " [x] Sent %r:%r" % (severity, message)

connection.close()
