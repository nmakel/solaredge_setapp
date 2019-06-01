import solaredge_setapp
import solaredge_setapp.status_pb2


class Status:
    
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
            # dict optimizers {int total, int online}
            # dict temperature {int value, {bool celsius, bool fahrenheit}}
            # int fan
            # str error
            # int subsystem_id
            # str bad_position
        # ]
    
        try:
            proto = solaredge_setapp.status_pb2.Status()
            proto.ParseFromString(bytes)
            parsed = {}

            parsed["serial"] = str(proto.serial)
            parsed["power_ac"] = float(proto.power_ac)
            parsed["voltage_ac"] = float(proto.voltage_ac)
            parsed["frequency"] = float(proto.frequency)
            parsed["monitoring"] = bool(proto.monitoring)
            
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
                    "fan": int(inverter.fan),
                    "error": str(inverter.error),
                    "subsystem_id": int(inverter.subsystem_id),
                    "bad_position": str(inverter.bad_position)
                })
        except AttributeError as e:
            print("AttributeError: {e}".format(e=e))

        return parsed