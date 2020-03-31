import solaredge_setapp
import solaredge_setapp.maintenance_pb2

import datetime


class Maintenance:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):

        parsed = {}

        try:
            proto = solaredge_setapp.maintenance_pb2.Maintenance()
            proto.ParseFromString(bytes)
            
            parsed = {
                "serial": str(proto.header.id),
                "timestamp": int(proto.header.timestamp),
                "standby": bool(proto.standby.activated),
                "utc_offset": int(proto.date_and_time.gmt_offset),
                "ntp_server": str(proto.date_and_time.ntp),
                "afci": {
                    "enabled": bool(proto.afci.enable),
                    "manual_reconnect": bool(proto.afci.manual_reconnect),
                    "test_result": int(proto.afci.test.result)
                },
            }

            parsed["inverters"] = []

            for inverter in proto.diagnostics.inverters.primary, proto.diagnostics.inverters.left, proto.diagnostics.inverters.right:
                if inverter.inv_sn:

                    if inverter.isolation.r_iso.scaling:
                        inverter_isolation_r_iso = float(inverter.isolation.r_iso.value / inverter.isolation.r_iso.scaling)
                    else:
                        inverter_isolation_r_iso = float(inverter.isolation.r_iso.value)

                    if inverter.isolation.alpha.scaling:
                        inverter_isolation_alpha = float(inverter.isolation.alpha.value / inverter.isolation.alpha.scaling)
                    else:
                        inverter_isolation_alpha = float(inverter.isolation.alpha.value)

                    parsed["inverters"].append({
                        "serial": str(inverter.inv_sn),
                        "isolation": {
                            "fault_location": int(inverter.isolation.fault_location),
                            "r_iso": inverter_isolation_r_iso,
                            "alpha": inverter_isolation_alpha
                        },
                        "optimizers_status": {
                            "total": int(inverter.optimizers_status.enabled),
                            "online": int(inverter.optimizers_status.connected)
                        },       
                        "optimizers": [{
                            "serial": str(po.sn),
                            "online": bool(po.reports),
                            "po_voltage": int(po.output_v),
                            "po_power": int(po.energy.value),
                            "module_voltage": int(po.input_v),
                            "module_current": int(po.input_c),
                            "temperature": int(po.temperature.value),
                            "timestamp": 0 if not bool(po.reports) else int(datetime.datetime.strptime(
                                "{year} {month} {day} {hour} {minutes} {seconds}".format(
                                year=po.date.year,
                                month=po.date.month,
                                day=po.date.day,
                                hour=po.date.hour,
                                minutes=po.date.minute,
                                seconds=po.date.second
                            ), "%Y %m %d %H %M %S").timestamp())
                        } for po in inverter.optimizer]
                })
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed
