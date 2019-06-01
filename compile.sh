#!/usr/bin/env sh

rm solaredge_setapp/*_pb2.py
protoc --proto_path=./messages --python_out=solaredge_setapp/ messages/*.proto
