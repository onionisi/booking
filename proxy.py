#!/usr/bin/env python2
# coding=utf-8

import zmq

context = zmq.Context()
front = context.socket(zmq.PULL)
front.bind("tcp://*:5564")

back = context.socket(zmq.PUB)
back.bind("tcp://*:5565")

while True:
    zmq.device(zmq.QUEUE, front, back)
