#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import time
import grpc

import exec_slave_pb2


def send_blocking(message):
    channel = grpc.insecure_channel('localhost:50051')
    stub = exec_slave_pb2.ExecSlaveStub(channel)
    request = exec_slave_pb2.ExecuteRequest(message=message)
    response = stub.Execute(request)
    print("Exec client send and recieve blocking response: " + response.message)
    return response


def send_nonblocking(message):
    channel = grpc.insecure_channel('localhost:50051')
    stub = exec_slave_pb2.ExecSlaveStub(channel)
    request = exec_slave_pb2.ExecuteRequest(message=message)
    future = stub.Execute.future(request)
    print("Exec client send request")
    return future


def recieve(future):
    response = future.result()
    print("Exec client received response: " + response.message)
    return response


def cancel(future):
    ret = future.cancel()
    print("Return of future.cancel() is {}".format(ret))
    channel = grpc.insecure_channel('localhost:50051')
    stub = exec_slave_pb2.ExecSlaveStub(channel)
    request = exec_slave_pb2.CancelRequest()
    response = stub.Cancel(request)
    print("Exec client send cancel and recieve recieve: " + response.message)


def run():
    # Blocking
    response = send_blocking("Blocking request.")

    # Non-blocking
    future = send_nonblocking("Non-blocking request and wait until finish.")
    response = recieve(future)

    # Non-blocking request cancel immediately
    future = send_nonblocking("Non-blocking request and cancel immediately.")
    cancel(future)

    # Non-blocking request cancel in computing
    future = send_nonblocking("Non-blocking request cancel in computing.")
    time.sleep(1)
    cancel(future)

    # Non-blocking request cancel after computing
    future = send_nonblocking("Non-blocking request cancel after computing.")
    time.sleep(7)
    cancel(future)


if __name__ == '__main__':
    run()
