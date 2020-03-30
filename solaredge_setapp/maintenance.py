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
                "utc_offset": int(proto.dateAndTime.gmtOffset),
                "ntp_server": str(proto.dateAndTime.ntp),
                "afci": {
                    "enabled": bool(proto.afci.enable),
                    "manual_reconnect": bool(proto.afci.manualReconnect),
                    "test_result": int(proto.afci.test.result)
                },
            }

            parsed["inverters"] = []

            for inverter in proto.diagnostics.inverters.primary, proto.diagnostics.inverters.left, proto.diagnostics.inverters.right:
                if inverter.invSn:

                    if inverter.isolation.rIso.scaling:
                        inverter_isolation_r_iso = float(inverter.isolation.rIso.value / inverter.isolation.rIso.scaling)
                    else:
                        inverter_isolation_r_iso = float(inverter.isolation.rIso.value)

                    if inverter.isolation.alpha.scaling:
                        inverter_isolation_alpha = float(inverter.isolation.alpha.value / inverter.isolation.alpha.scaling)
                    else:
                        inverter_isolation_alpha = float(inverter.isolation.alpha.value)

                    parsed["inverters"].append({
                        "serial": str(inverter.invSn),
                        "isolation": {
                            "fault_location": int(inverter.isolation.faultLocation),
                            "r_iso": inverter_isolation_r_iso,
                            "alpha": inverter_isolation_alpha
                        },
                        "optimizers_status": {
                            "total": int(inverter.optimizersStatus.enabled),
                            "online": int(inverter.optimizersStatus.connected)
                        },       
                        "optimizers": [{
                            "serial": str(po.sn),
                            "online": bool(po.reports),
                            "po_voltage": int(po.outputV),
                            "module_voltage": int(po.inputV),
                            "module_current": int(po.inputC),
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
                        } for po in inverter.optimizerList]
                })
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed
