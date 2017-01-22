#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import time
import grpc

import helloworld_pb2


def send_blocking():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2.GreeterStub(channel)
    request = helloworld_pb2.HelloRequest(name='you')
    response = stub.SayHello(request)
    print("Greeter client recieve blocking response")
    return response


def send_nonblocking():
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
    print("Return of future.cancel() is {}".format(ret))
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2.GreeterStub(channel)
    request = helloworld_pb2.CancelRequest()
    response = stub.Cancel(request)
    print("Greeter client send cancel")


def run():
    # Blocking
    response = send_blocking()

    # Non-blocking
    future = send_nonblocking()
    response = recieve(future)

    # Non-blocking send cancel immediately
    future = send_nonblocking()
    cancel(future)

    # Non-blocking send cancel in computing
    future = send_nonblocking()
    time.sleep(1)
    cancel(future)

    # Non-blocking send cancel after computing
    future = send_nonblocking()
    time.sleep(7)
    cancel(future)


if __name__ == '__main__':
    run()
