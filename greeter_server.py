#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time

import time
import grpc

import helloworld_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2.GreeterServicer):

    def SayHello(self, request, context):
        print("Greeter server received request")
        time.sleep(10)
        print("Greeter server send response")
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        print("Greeter server received request")
        print("Greeter server send response")
        return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
