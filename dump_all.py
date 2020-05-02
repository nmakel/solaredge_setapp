#!/usr/bin/env python3

import solaredge_setapp
import argparse
import json
import requests


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("address", type=str, help="hostname or ip address of solaredge inverter")
    args = argparser.parse_args()

    data = {}
    web_services = [
        # name, endpoint_url, module_class, data_name
        ("Maintenance", "web/v1/maintenance", solaredge_setapp.maintenance.Maintenance(), "maintenance"),
        ("Information", "web/v1/information", solaredge_setapp.information.Information(), "information"),
        ("Status", "web/v1/status", solaredge_setapp.status.Status(), "status")
    ]

    try:
        for name, endpoint_url, module_class, data_name in web_services:
            endpoint_request = requests.get(f"http://{args.address}/{endpoint_url}")

            if endpoint_request.status_code != 200:
                raise Exception(f"Unable to load '{name}' at {endpoint_url}")

            print(f"\n{name} http://{args.address}/{endpoint_url}")
            print(json.dumps(module_class.parse_protobuf(endpoint_request.content), indent=4))
    except TypeError:
        print(f"Parsing of http://{args.address}/{endpoint_url} failed!")
    except requests.exceptions.ConnectionError:
        print(f"Could not connect to SetApp on {args.address}")
