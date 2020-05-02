#!/usr/bin/env python3

import solaredge_setapp
import argparse
import datetime
import requests


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("address", type=str, help="hostname or ip address of solaredge inverter")
    args = argparser.parse_args()

    address = args.address

    data = {}
    web_services = [
        # name, endpoint_url, module_class, data_name
        ("Information", "web/v1/information", solaredge_setapp.information.Information(), "information"),
        ("Maintenance", "web/v1/maintenance", solaredge_setapp.maintenance.Maintenance(), "maintenance"),
        ("Status", "web/v1/status", solaredge_setapp.status.Status(), "status")
    ]

    try:
        for name, endpoint_url, module_class, data_name in web_services:
            endpoint_request = requests.get(f"http://{args.address}/{endpoint_url}")

            if endpoint_request.status_code != 200:
                raise Exception(f"Unable to load '{name}' at {endpoint_url}")

            data[data_name] = module_class.parse_protobuf(endpoint_request.content)

        if "information" in data:
            print("\n\tCPU {cpu} | DSP1: {dsp1} | DSP2: {dsp2}".format(
                cpu=data["information"]["cpu"],
                dsp1=data["information"]["dsp1"],
                dsp2=data["information"]["dsp2"]
            ))

        if "status" in data:
            for inverter in data["status"]["inverters"]:
                print("\n\t{serial}\t{status}\t{temperature}°C".format(
                    serial=inverter["serial"],
                    status=data["status"]["status"],
                    temperature=inverter["temperature"]["value"]
                ))

            print("\n\t{power_ac:7.2f}W\t{production_today:.2f}kWh ∑ {production_total:.2f}kWh".format(
                power_ac=data["status"]["power_ac"],
                production_today=(data["status"]["energy"]["day"] / 1000),
                production_total=(data["status"]["energy"]["total"] / 1000)
            ))

            print("\n\t⏦ {voltage_ac:.2f}Vac @ {frequency:.2f}Hz".format(
                voltage_ac=data["status"]["voltage_ac"],
                frequency=data["status"]["frequency"],
            ))

            print("\t⎓ {voltage_dc:.2f}Vdc".format(
                voltage_dc=data["status"]["inverters"][0]["voltage_dc"],
            ))

        if "maintenance" in data:
            pos = []
            parsed = []

            for inverter in data["maintenance"]["inverters"]:
                if not inverter["serial"]:
                    continue

                print("\n\tPower optimizers ({online}/{total}) connected to {serial}:".format(
                    online=inverter["optimizers_status"]["online"],
                    total=inverter["optimizers_status"]["total"],
                    serial=inverter["serial"]
                ))

                for po in inverter["optimizers"]:
                    print("\n\t{serial}\t{last_report}".format(
                        serial=po["serial"],
                        last_report=datetime.datetime.fromtimestamp(po["timestamp"]).strftime("%Y-%m-%d %H:%M:%S") if po["online"] else "Offline",
                    ), end="")

                    if po["online"]:
                        print("\t{temperature:2.0f}°C\t{module_voltage:4.1f}V\t{module_current:4.1f}A\t{po_voltage:4.1f}V\t{po_power:3.0f}W".format(
                            temperature=po["temperature"],
                            module_voltage=po["module_voltage"],
                            module_current=po["module_current"],
                            po_voltage=po["po_voltage"],
                            po_power=(po["module_voltage"] * po["module_current"])
                        ), end="")

        print("")
    except requests.exceptions.ConnectionError:
        print(f"Could not connect to SetApp on {args.address}")
