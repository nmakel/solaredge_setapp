#!/usr/bin/env sh

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "Usage: $0 wsa-version"

rm solaredge_setapp/*_pb2.py
protoc --proto_path=messages/$1/ --python_out=solaredge_setapp/ messages/$1/*.proto