#!/usr/bin/env python
import pika, sys

"""allows messages to be funneled into either "info", warning", or "error" depending on their severity"""

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates direct exchange
channel.exchange_declare(exchange='direct_logs', type='direct')

#creates queue
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

#severities are cmd line arg
severities = sys.argv[1:]
#if none given, error message
"""if not severities:
        print >> sys.stderr, "Usage: %s [info] [warning] [error]" % \ (sys.argv[0],)
        sys.exit(1)
"""
#for each severity, create a separate bind with its key
for severity in severities:
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print ' [*] Waiting for logs. To exit press CTRL+C'

#I'm assuming method.routing_key translates the severity key somehow
def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
