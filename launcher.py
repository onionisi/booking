#!/usr/bin/env python2
# coding=utf-8
#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
import message_pb2
import time

class Lancher:
    def __init__(self):
        context = zmq.Context()

        sync = context.socket(zmq.PUSH)
        sync.bind("tcp://localhost:5565")

    def send_data(self, data):

        message = message_pb2.Order()
        # data
        message.name=data['name'].encode('utf8')
        message.phone=data['phone'].encode('utf8')
        message.addr=data['addr'].encode('utf8')
        message.time=data['time']
        message.cost=data['cost']
        message.pay=data['pay']

        for each in data['order']:
            message.good.append(each.encode('utf8'))

        # data type
        store = "onionisi"
        msg_str=message.SerializeToString()

        self.socket.send_multipart([store, msg_str])
