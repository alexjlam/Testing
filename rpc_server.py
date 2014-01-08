#!/usr/bin/env python

"""creates connection and rpc queue
   on server side, creates response of fibonacci number
   sends response back to reply_to and correlation_id"""

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates rpc queue (outgoing)
channel.queue_declare(queue='rpc_queue')

#determines nth fibonacci number
def fib(n):
        if n == 0:
                return 0
        elif n == 1:
                return 1
        else:
                return fib(n-1) + fib(n-2)

#executed when request is received, does the work and sends response back
def on_request(ch, method, props, body):
        #creates a response of the nth number given for the fibonacci sequence
        n = int(body)
        print " [.] fib(%s)" % (n,)
        response = fib(n)

        #publishes message with reply_to (set to callback) and correlation_id, and will ack as well
        #sends response back (does the work part)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

#basic_qos will not dispatch a new request until its completed and ack the previous request
channel.basic_qos(prefetch_count=1)

#on_request receives requests from rpc_queue (at server?)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()

