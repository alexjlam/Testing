#!/usr/bin/env python

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates topic exchange
channel.exchange_declare(exchange='topic_logs', type='topic')

#creates randomly generated queue
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
#if no binding_key is given, produce error output
if not binding_keys:
        print >> sys.stderr, "Usage: %s [binding_key]..." % (sys.argv[0],)
        sys.exit(1)

#creates binds between topic_logs exchange an a random queue with the binding_key for each key
#assuming queue_bind translates the routing_key so it can somehow match its respective routing_key
for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback (ch, method, properties, body):
        print " [x] %r:%r" % (method.routing_key, body,)

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
