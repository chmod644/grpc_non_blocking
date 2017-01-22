# Makefile

SRC=helloworld.proto

all: $(SRC)
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $(SRC)

clean:
	rm -rf *_pb2*.py *.pyc
