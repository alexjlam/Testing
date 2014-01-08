#!/usr/bin/env python

"""creates connection, callback queue going to on_response
   on_response will check correlation_id for match
   call will publish a message with a reply_to (to rpc queue) and new generated corr_id
   waits for proper response and then returns the response
"""

import pika, uuid

class FibonacciRpcClient(object):
        #initializer that establishes connection, creates callback_queue, on_response to receive from callback_queue
        #subscribe to callback_queue so that we can receive RPC responses
        def __init__(self):
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                self.channel = self.connection.channel()
                result = self.channel.queue_declare(exclusive=True)
                self.callback_queue = result.method.queue
                self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

        #executed on every response, checks correlation_id with the one we're looking for
        #if it's a match, it'll save the response
        def on_response(self, ch, method, props, body):
                if self.corr_id == props.correlation_id:
                        self.response = body

        def call (self, n):
                self.response = None
                #generates and saves unique corr_id to match in on_response
                self.corr_id = str(uuid.uuid4())
                #publishes request message with reply_to to rpc_queue and new corr_id
                self.channel.basic_publish(exchange='',
                                        routing_key='rpc_queue',
                                        properties=pika.BasicProperties(
                                                reply_to=self.callback_queue,
                                                correlation_id = self.corr_id),
                                        body=str(n))
                #waits for proper response
                while self.response is None:
                        self.connection.process_data_events()
                #when it receives the proper response, returns response back
                return int(self.response)

fibonacci_rpc = FibonacciRpcClient()
print " [x] Requesting fib(30)"
response = fibonacci_rpc.call(30)
print " [.] Got %r" % (response,)
