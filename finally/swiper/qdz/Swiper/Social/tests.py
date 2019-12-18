#!/usr/bin/env python

from django.test import TestCase
import pika
# Create your tests here.

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange="fanout_logs", exchange_type="fanout")

message = 'Hello world'

channel.basic_publish(exchange='fanout_logs', routing_key='', body=message)


print('发送信息:', message)
connection.close()