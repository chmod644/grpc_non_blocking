#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import time
import grpc

import helloworld_pb2


def send():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2.GreeterStub(channel)
    request = helloworld_pb2.HelloRequest(name='you')
    future = stub.SayHello.future(request)
    print("Greeter client send request")
    return future


def recieve(future):
    response = future.result()
    print("Greeter client received response: " + response.message)
    return response


def cancel(future):
    ret = future.cancel()
    print("Greeter client send cancel")


def run():
    future1 = send()
    future2 = send()
    time.sleep(1)
    cancel(future1)
    response = recieve(future2)


if __name__ == '__main__':
    run()
