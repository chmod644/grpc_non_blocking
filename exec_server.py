#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent import futures
import time

import time
import subprocess
import grpc

import exec_slave_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Executer(exec_slave_pb2.ExecSlaveServicer):

    def __init__(self):
        self.proc = None

    def Execute(self, request, context):
        print("Exec server received request: " + request.message)
        self.proc = subprocess.Popen(["python", "slave.py"])
        status = self.proc.wait()
        message = 'Exit status is {}.'.format(status)
        print("Exec server send response: " + message)
        self.proc = None
        return exec_slave_pb2.ExecuteReply(message=message)

    def Cancel(self, request, context):
        print("Exec server received cancel request.")
        if self.proc is not None:
            self.proc.kill()
            message = "Exec is killed."
        else:
            message = "Slave process has not been started or finished."
        print(message)
        print("Exec server send calcel response.")
        return exec_slave_pb2.CancelReply(message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    exec_slave_pb2.add_ExecSlaveServicer_to_server(Executer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
