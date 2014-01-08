#!/usr/bin/python

import pika
import time

#establishes connection to RabbitMQ server as before
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#creates queue
#queue is made "durable" so as to not lose queue or message if RabbitMQ crashes
channel.queue_declare(queue='task_queue', durable=True)

#waits for data in a infinite loop and runs callbacks whenever necessary
print ' [*] Waiting for messages. To exit press CTRL+C'

#when a message is received, callback is called by the Pika library and prints the contents of the message
#sleeps for one second per dot in message
def callback(ch, method, properties, body):
        print " [x] Received %r" % (body,)
        time.sleep(body.count('.'))
        print " [x] Done"
        #consumer sends ack to RabbitMQ to let it know that a message was received
        ch.basic_ack(delivery_tag = method.delivery_tag)

#will not dispatch a new message to a worker until it has processed and acknowledged the previous one
#dispatches to next worker that is not busy
channel.basic_qos(prefetch_count=1)

#tells RabbitMQ that this callback function receives messages from the hello queue
channel.basic_consume(callback, queue='task_queue')
channel.start_consuming()


