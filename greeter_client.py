#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import grpc

import helloworld_pb2


def send():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2.GreeterStub(channel)
    request = helloworld_pb2.HelloRequest(name='you')
    future = stub.SayHello.future(request)
    return future


def recieve(future):
    response = future.result()
    return response


def run():
    future = send()
    print("Greeter client send request")
    response = recieve(future)
    print("Greeter client received response: " + response.message)


if __name__ == '__main__':
    run()
