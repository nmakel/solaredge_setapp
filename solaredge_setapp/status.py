import solaredge_setapp
import solaredge_setapp.status_pb2


class Status:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):
        
        # str serial
        # float power_ac
        # float voltage_ac
        # float frequency
        # bool monitoring
        # str status from enum solaredge_setapp.Status
        # bool switch
        # float cosphi
        # float power_ac_limit
        # int country_id
        # str country from enum solaredge_setapp.Countries
        # str portia_error
        # int portia_subsystem_id
        # dict optimizers {int total, int online}
        # dict energy {float day, float month, float year, float total}
        # list inverters [
            # str serial": inverter.serial,
            # float voltage_dc": inverter.voltage_dc,
            # dict isolation {int fault_location, int isolation, int alpha}
            # dict optimizers {int total, int online}
            # dict temperature {int value, {bool celsius, bool fahrenheit}}
            # int fan
            # str error
            # int subsystem_id
            # str bad_position
        # ]
    
        parsed = {}

        try:
            proto = solaredge_setapp.status_pb2.Status()
            proto.ParseFromString(bytes)
            
            parsed = {
                "serial": str(proto.serial),
                "power_ac": float(proto.power_ac),
                "voltage_ac": float(proto.voltage_ac),
                "frequency": float(proto.frequency),
                "monitoring": bool(proto.monitoring),
                "afci": {
                    "enabled": proto.afci.enabled,
                    "manual_reconnect": proto.afci.manual_reconnect
                }
            }

            try:
                parsed["status"] = solaredge_setapp.Status(int(proto.status)).name
            except ValueError as e:
                parsed["status"] = solaredge_setapp.Status(-1).name

            parsed["switch"] = bool(proto.switch)
            parsed["cosphi"] = float(proto.cosphi)
            parsed["power_ac_limit"] = int(proto.power_ac_limit)
            parsed["country_id"] = int(proto.country)
            
            try:
                parsed["country"] = solaredge_setapp.Countries(parsed["country_id"]).name
            except ValueError as e:
                parsed["country"] = solaredge_setapp.Countries(-1).name
    
            parsed["portia_error"] = str(proto.portia_error)
            parsed["portia_subsystem_id"] = int(proto.portia_subsystem)
    
            parsed["optimizers"] = {
                "total": int(proto.optimizers.total),
                "online": int(proto.optimizers.online)
            }

            parsed["server_communication"] = {
                "physical": bool(proto.server_communication.status.physical),
                "ip": bool(proto.server_communication.status.ipaddress),
                "gateway": bool(proto.server_communication.status.gateway),
                "internet": bool(proto.server_communication.status.internet),
                "monitoring": bool(proto.server_communication.status.monitoring),
                "server": bool(proto.server_communication.status.server)
            }

            parsed["communication"] = {
                "lan": {
                    "mac": proto.communication.lan.mac.value,
                    "dhcp": bool(proto.communication.lan.dhcp.value),
                    "ip": proto.communication.lan.ip.ip.value,
                    "netmask": proto.communication.lan.ip.netmask.value,
                    "gateway": proto.communication.lan.ip.gateway.value,
                    "dns": proto.communication.lan.ip.dns.value,
                    "connected": bool(proto.communication.lan.connected.value)
                }
            }

            parsed["energy"] = {
                "day": float(proto.energy.day),
                "month": float(proto.energy.month),
                "year": float(proto.energy.year),
                "total": float(proto.energy.total)
            }

            parsed["inverters"] = []

            for inverter in proto.inverters.primary, proto.inverters.left, proto.inverters.right:
                if not inverter.serial:
                    continue

                parsed["inverters"].append({
                    "serial": str(inverter.serial),
                    "voltage_dc": float(inverter.voltage_dc),
                    "optimizers": {
                        "total": int(inverter.optimizers.total),
                        "online": int(inverter.optimizers.online)
                    },
                    "temperature": {
                        "value": int(inverter.temperature.value),
                        "unit": {
                            "celsius": bool(inverter.temperature.units.celsius),
                            "fahrenheit": bool(inverter.temperature.units.fahrenheit)
                        }
                    },
                    "isolation": {
                        "fault_location": int(inverter.isolation.fault_location),
                        "isolation": int(inverter.isolation.r_iso.isolation),
                        "alpha": int(inverter.isolation.alpha.isolation)
                    },
                    "fan": int(inverter.fan),
                    "error": str(inverter.error),
                    "subsystem_id": int(inverter.subsystem_id),
                    "bad_position": str(inverter.bad_position)
                })
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed