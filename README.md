# solaredge_setapp

solaredge_setapp is a python library that parses inverter and power optimizer data from a compatible SolarEdge PV inverter. Only those models which support SetApp commissioning are supported.

This project is built on the efforts of others: for Home Assistant users, see drobstravels' <a href="https://github.com/drobstravels/solaredge_local">solaredge_local</a>, and jbuehl's <a href="https://github.com/jbuehl/solaredge">solaredge</a> for all non-SetApp power inverters.

## Installation

The library is not yet available on PyPi. Until then, clone the repository and import the library `solaredge_setapp` locally.

`solaredge_setapp` uses Python3's standard library, and Google's `protobuf`. The example script further depends on `argparse` and `requests`. 

In order to use `compile.sh` to compile the protocol buffer `.proto` message definitions you will need `protoc`, which is provided, for example, by Ubuntu's package `protobuf-compiler`. Re-compiling the messages is only necessary if you have made changes to them.

## Usage

See `example.py` how to fetch, parse, and display the SetApp protobuf files exposed by the SetApp API. Basic usage involves:

```
import solaredge_setapp
import requests

inverter_ip = "10.0.0.1"
status_bytes = requests.get("http://{0}/web/v1/status".format(inverter_ip)).content
status = solaredge_setapp.status.Status()
status_data = status.parse_protobuf(status_bytes) 

print("Inverter {serial} is {status} at {power_ac:.2f}W".format(
    serial=status_data["serial"],
    status=status_data["status"],
    power_ac=status_data["power_ac"]
))
```

## Contributing

Contributions are more than welcome, especially to the protocol buffer message definitions.