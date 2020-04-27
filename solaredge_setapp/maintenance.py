import solaredge_setapp
import solaredge_setapp.maintenance_pb2

import datetime


class Maintenance:

    def parse_protobuf(self, bytes):
        parsed = {}

        try:
            proto = solaredge_setapp.maintenance_pb2.Maintenance()
            proto.ParseFromString(bytes)

            parsed = {
                "serial": str(proto.header.id),
                "timestamp": int(proto.header.timestamp),
                "standby": bool(proto.standby.activated.value),
                "utc_offset": int(proto.date_and_time.gmt_offset.value),
                "ntp_server": str(proto.date_and_time.ntp.value),
                "afci": {
                    "enabled": bool(proto.afci.enable.value),
                    "manual_reconnect": bool(proto.afci.manual_reconnect.value),
                    "test_result": solaredge_setapp.AfciTestResult(int(proto.afci.test.result)).name
                },
            }

            parsed["inverters"] = []

            for inverter in proto.diagnostics.inverters.primary, proto.diagnostics.inverters.left, proto.diagnostics.inverters.right:
                if inverter.inv_sn.value:

                    if inverter.isolation.r_iso.scaling:
                        inverter_isolation_r_iso = float(inverter.isolation.r_iso.value / inverter.isolation.r_iso.scaling)
                    else:
                        inverter_isolation_r_iso = float(inverter.isolation.r_iso.value)

                    if inverter.isolation.alpha.scaling:
                        inverter_isolation_alpha = float(inverter.isolation.alpha.value / inverter.isolation.alpha.scaling)
                    else:
                        inverter_isolation_alpha = float(inverter.isolation.alpha.value)

                    parsed["inverters"].append({
                        "serial": str(inverter.inv_sn.value),
                        "isolation": {
                            "fault_location": int(inverter.isolation.fault_location.value),
                            "r_iso": inverter_isolation_r_iso,
                            "alpha": inverter_isolation_alpha
                        },
                        "optimizers_status": {
                            "total": int(inverter.optimizers_status.enabled.value),
                            "online": int(inverter.optimizers_status.connected.value)
                        },
                        "optimizers": [{
                            "serial": str(po.sn.value),
                            "online": bool(po.reports.value),
                            "po_voltage": int(po.output_v.value),
                            "po_power": int(po.energy.value),
                            "module_voltage": int(po.input_v.value),
                            "module_current": int(po.input_c.value),
                            "temperature": int(po.temperature.value.value),
                            "timestamp": 0 if not bool(po.reports.value) else int(datetime.datetime.strptime(
                                "{year} {month} {day} {hour} {minutes} {seconds}".format(
                                    year=po.date.year.value,
                                    month=po.date.month.value,
                                    day=po.date.day.value,
                                    hour=po.date.hour.value,
                                    minutes=po.date.minute.value,
                                    seconds=po.date.second.value
                                ), "%Y %m %d %H %M %S").timestamp())
                        } for po in inverter.optimizer]
                    })
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed
