# solaredge_setapp

solaredge_setapp is a python library that parses inverter and power optimizer data from a compatible SolarEdge PV inverter. Only those models which support SetApp commissioning are supported.

This project is built on the efforts of others: for Home Assistant users, see drobtravels' <a href="https://github.com/drobtravels/solaredge-local">solaredge_local</a>, and jbuehl's <a href="https://github.com/jbuehl/solaredge">solaredge</a> for all non-SetApp power inverters.

Developed and tested on a European SE3500H-RW000BNN4 SolarEdge single-phase inverter -- CPU versions 4.7.26, 4.6.24 and 4.5.41, and WSA 1.3.9, 1.2.9 and 1.1.12. It may work on older, or newer, versions of SetApp.

Release 0.0.6 and earlier are compatible with WSA <= 1.3.9.

## Installation

To install, either clone this project and install using `distutils`:

```python3 setup.py install```

or install the package from PyPi:

```pip3 install solaredge_setapp```

## Usage

See `example.py` how to fetch, parse, and display the SetApp protobuf files exposed by the SetApp API.

```python3 example.py your-inverter-ip```

For a complete json dump of all parsed values from all endpoints, try `dump_all.py`:

```python3 dump_all.py your-inverter-ip```

Basic usage of the **status** API endpoint:

```
import solaredge_setapp
import requests

inverter_ip = "10.0.0.1"

status_request = requests.get(f"http://{inverter_ip}/web/v1/status").content
status = solaredge_setapp.status.Status(status_request)

print(f"Inverter {status['serial']} is {status['status']} at {status['power_ac']:.2f}W")
```

See the relevant `.proto` file in `solaredge_setapp/messages/`, and `solaredge_setapp/%endpoint%.py` for all fields that are parsed for that particular endpoint.

The following API endpoints contain most of the useful information, and are therefore the primary focus:

* **information** - web/v1/information - CPU and DSP versions, error logging
* **maintenance** - web/v1/maintenance - power optimizer telemetry
* **status** - web/v1/status - inverter and energy statistics

The remaining endpoints mostly concern functionality of the commissioning interface itself, and are therefore not implemented:

* **app_configs** - web/v1/app_configs - language and functionality
* **communication** - web/v1/communication - ethernet, wifi and RS485 settings
* **grid_protection** - web/v1/grid_protection - grid protection settings
* **power_control** - web/v1/power_control - grid power settings
* **region** - web/v1/region - language and country settings


## Working on protobuf messages

In order to use `compile_proto.sh` to (re)compile the protocol buffer `.proto` message definitions you will need `protoc`, which is provided, for example, by Ubuntu's `protobuf-compiler` package. *(Re-)compiling the protobuf messages is only necessary if you have made local changes to them.*

You can test changes to .proto files directly by passing raw protobufs to `protoc`:

```curl -s http://your-inverter-ip/web/v1/status | protoc --decode Status messages/status.proto```

## Limitations

The SetApp API does not (yet) provide real-time power optimizer data. Initial results suggest the data is 5-15 minutes old. Inverter production and voltage information is near real-time, however. Basically, the entire information set visible on the inverter's SetApp web interface is available through this library, in addition to per optimizer voltages and temperatures. Power optimizer voltages and current are expressed as integers, and are therefore not entirely accurate.

Rate limiting will kick in if you have the SetApp web interface open while using this library.

The SetApp API is new, and therefore likely to change. Variable naming, distribution, and parsing is likely to change.

## Contributing

Contributions are more than welcome, especially to the protocol buffer message definitions.
