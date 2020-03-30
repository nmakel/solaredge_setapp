#!/usr/bin/env python3

import solaredge_setapp
import argparse
import datetime
import json
import requests


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("address", type=str, help="hostname or ip address of solaredge inverter")
    parserargs = argparser.parse_args()

    data = {}
    web_services = [
        ("Region", "web/v1/region", solaredge_setapp.region.Region(), "region"),
        ("Communication", "web/v1/communication", solaredge_setapp.communication.Communication(), "communication"),
        ("Power Control", "web/v1/power_control", solaredge_setapp.power_control.PowerControl(), "power_control"),
        ("Maintenance", "web/v1/maintenance", solaredge_setapp.maintenance.Maintenance(), "maintenance"),
        ("Information", "web/v1/information", solaredge_setapp.information.Information(), "information"),
        ("WebAppConfigs", "web/v1/app_configs", solaredge_setapp.app_configs.WebAppConfigs(), "app_configs"),
        ("Status", "web/v1/status", solaredge_setapp.status.Status(), "status"),
        ("Grid Protection", "web/v1/grid_protection", solaredge_setapp.grid_protection.GridProtection(), "grid_protection"),
    ]

    try:
        for name, endpoint_url, module_class, data_name in web_services:
            endpoint_request = requests.get(f"http://{parserargs.address}/{endpoint_url}")

            if endpoint_request.status_code != 200:
                raise Exception(f"Unable to load '{name}' at {endpoint_url}")

            print(f"\n{name} http://{parserargs.address}/{endpoint_url}")
            print(json.dumps(module_class.parse_protobuf(endpoint_request.content), indent=4))
    except TypeError:
        print(f"Parsing of http://{parserargs.address}/{endpoint_url} failed!")
    except requests.exceptions.ConnectionError:
        print(f"Could not connect to SetApp on {parserargs.address}")