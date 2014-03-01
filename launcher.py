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
        
        # sync = context.socket(zmq.PULL)
        # sync.bind("tcp://*:5564")
        
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5565")
        
        # socket.setsockopt(zmq.HWM, 1)

    def send_data(self, data):
        # sync_request = sync.recv()
        
        message = message_pb2.Order()

        message.name=data['name'].encode('utf8')
        message.phone=data['phone'].encode('utf8')
        message.addr=data['addr'].encode('utf8')
        for each in data['order']:
            message.good.append(each.encode('utf8'))
        
        msg_str=message.SerializeToString()
        
        for i in xrange(2):
            store = "onionisi"
            self.socket.send_multipart([store, msg_str])
            time.sleep(0.2)
