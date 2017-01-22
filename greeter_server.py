#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time

import time
import subprocess
import grpc

import helloworld_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2.GreeterServicer):

    def __init__(self):
        self.proc = None

    def SayHello(self, request, context):
        print("Greeter server received request")
        self.proc = subprocess.Popen(["python", "slave.py"])
        while self.proc.poll() is None:
            time.sleep(0.1)
        status = self.proc.poll()
        message = 'Hello, {}! Status is {}.'.format(request.name, status)
        print("Greeter server send response: " + message)
        self.proc = None
        return helloworld_pb2.HelloReply(message=message)

    def Cancel(self, request, context):
        print("Greeter server received cancel")
        if self.proc is not None:
            self.proc.kill()
            print("Greeter is killed")
        else:
            print("Greeter has not been started or finished.")
        return helloworld_pb2.CancelReply()

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
