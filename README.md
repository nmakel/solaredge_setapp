# solaredge_setapp

solaredge_setapp is a python library that parses inverter and power optimizer data from a compatible SolarEdge PV inverter. Only those models which support SetApp commissioning are supported.

This project is built on the efforts of others: for Home Assistant users, see drobtravels' <a href="https://github.com/drobtravels/solaredge-local">solaredge_local</a>, and jbuehl's <a href="https://github.com/jbuehl/solaredge">solaredge</a> for all non-SetApp power inverters.

## Installation

The library is not yet available on PyPi. Until then, clone the repository and install the package using `distutils`:

```python3 setup.py install```

`solaredge_setapp` uses Python3's standard library, and Google's `protobuf`. The example script further depends on `requests`. 

See `requirements.txt`, or use `pip3` to install any dependencies:

```pip3 install -r requirements.txt```

In order to use `compile.sh` to compile the protocol buffer `.proto` message definitions you will need `protoc`, which is provided, for example, by Ubuntu's package `protobuf-compiler`. *Re-compiling the messages is only necessary if you have made changes to them.*

## Usage

See `example.py` how to fetch, parse, and display the SetApp protobuf files exposed by the SetApp API.

Basic usage of the **status** API endpoint:

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

See the `status.proto` file for all possible fields, and `solaredge_setapp/status.py`  for all fields that are parsed for this endpoint.

The following API endpoints are available:

* **app_configs** - language and functionality
* **communication** - ethernet, wifi and RS485 settings, **not yet implemented**
* **information** - CPU and DSP versions, error logging
* **maintenance** - power optimizer telemetry
* **power_control** - grid power settings, **not yet implemented**
* **region** - language and country settings
* **status** - inverter and energy statistics

## Limitations

The SetApp API does not (yet) provide real-time power optimizer data. Initial results suggest the data is 5-15 minutes old. Inverter production and voltage information is near real-time, however. Basically, the entire information set visible on the inverter's SetApp web interface is available through this library, in addition to per  optimizer voltages and temperatures.

Rate limiting will kick in if you have the SetApp web interface open while also polling using this library.

The SetApp API is new, and therefore likely to change.

## Contributing

Contributions are more than welcome, especially to the protocol buffer message definitions.