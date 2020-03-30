import solaredge_setapp
import solaredge_setapp.status_pb2


class Status:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):

        parsed = {}

        try:
            proto = solaredge_setapp.status_pb2.Status()
            proto.ParseFromString(bytes)
            
            parsed = {
                "serial": str(proto.sn),
                "power_ac": float(proto.powerWatt),
                "power_ac_limit": int(proto.limit),
                "voltage_ac": float(proto.voltage),
                "frequency": float(proto.frequencyHz),
                "status": int(proto.status),
                "switch": bool(proto.switchStatus),
                "cosphi": float(proto.cosPhi),
                "country_id": int(proto.country),
                "portia_subsystem_id": int(proto.portiaSubsystem),
                "afci": {
                    "enabled": bool(proto.afci.enable),
                    "manual_reconnect": bool(proto.afci.manualReconnect),
                    "test_result": int(proto.afci.test.result)
                },
                "optimizers": {
                    "total": int(proto.optimizersStatus.enabled),
                    "online": int(proto.optimizersStatus.connected)
                },
                "server_connection": bool(proto.sOk),
                "server_communication": {
                    "physical": bool(proto.serverComm.lanTest.physicalConnection),
                    "ip": bool(proto.serverComm.lanTest.ipAddress),
                    "gateway": bool(proto.serverComm.lanTest.gatewayLink),
                    "internet": bool(proto.serverComm.lanTest.internetLink),
                    "monitoring": bool(proto.serverComm.lanTest.monitoringLink),
                    "server": bool(proto.serverComm.lanTest.sOk)
                },
                "server_channel": {
                    "lan": bool(proto.serverChannel.lan.value),
                    "cellular": bool(proto.serverChannel.cellular.value),
                    "rs485_1": bool(proto.serverChannel.rs4851SeSlave.value),
                    "rs485_2": bool(proto.serverChannel.rs4852SeSlave.value),
                    "wifi": bool(proto.serverChannel.wifi.value),
                    "zigbee": bool(proto.serverChannel.zigbee.value) 
                },
                "energy": {
                    "day": float(proto.energy.today),
                    "month": float(proto.energy.thisMonth),
                    "year": float(proto.energy.thisYear),
                    "total": float(proto.energy.total)
                },
                "inverters": [],
                "meters": [],
                "batteries": [],
                "communication": {
                    "lan": {
                        "mac": str(proto.communication.lanInfo.mac.value),
                        "dhcp": bool(proto.communication.lanInfo.dhcp.value),
                        "ip": str(proto.communication.lanInfo.ip.ipAddress.value),
                        "netmask": str(proto.communication.lanInfo.ip.subnetMask.value),
                        "gateway": str(proto.communication.lanInfo.ip.gateway.value),
                        "dns": str(proto.communication.lanInfo.ip.dns.value),
                        "connected": bool(proto.communication.lanInfo.cableConnected.value)
                    },
                    "rs485_1": {
                        "protocol": {
                            "se_slave": bool(proto.communication.rs4851.protocol.seSlave),
                            "se_master": bool(proto.communication.rs4851.protocol.seMaster),
                            "modbus_multi_devices": bool(proto.communication.rs4851.protocol.modbusMultiDevices),
                            "sunspec": bool(proto.communication.rs4851.protocol.sunspec),
                            "none": bool(proto.communication.rs4851.protocol.none)
                        }
                    },
                    "rs485_2": {
                         "protocol": {
                            "se_slave": bool(proto.communication.rs4852.protocol.seSlave),
                            "se_master": bool(proto.communication.rs4852.protocol.seMaster),
                            "modbus_multi_devices": bool(proto.communication.rs4852.protocol.modbusMultiDevices),
                            "sunspec": bool(proto.communication.rs4852.protocol.sunspec),
                            "none": bool(proto.communication.rs4852.protocol.none)
                        }
                    }
                }
            }

            try:
                parsed["status"] = solaredge_setapp.Status(parsed["status"]).name
            except ValueError as e:
                parsed["status"] = solaredge_setapp.Status(-1).name

            try:
                parsed["country"] = solaredge_setapp.Countries(parsed["country_id"]).name
            except ValueError as e:
                parsed["country"] = solaredge_setapp.Countries(-1).name

            for inverter in proto.inverters.primary, proto.inverters.left, proto.inverters.right:
                if not inverter.dspSn:
                    continue

                if inverter.power.scaling:
                    inverter_power_ac = float(inverter.power.value / inverter.power.scaling)
                else:
                    inverter_power_ac = float(inverter.power.value)

                if inverter.isolation.rIso.scaling:
                    inverter_isolation_r_iso = float(inverter.isolation.rIso.value / inverter.isolation.rIso.scaling)
                else:
                    inverter_isolation_r_iso = float(inverter.isolation.rIso.value)

                if inverter.isolation.alpha.scaling:
                    inverter_isolation_alpha = float(inverter.isolation.alpha.value / inverter.isolation.alpha.scaling)
                else:
                    inverter_isolation_alpha = float(inverter.isolation.alpha.value)               

                parsed["inverters"].append({
                    "serial": str(inverter.dspSn),
                    "voltage_dc": float(inverter.voltage),
                    "power_ac": inverter_power_ac,
                    "optimizers": {
                        "total": int(inverter.optimizers.enabled),
                        "online": int(inverter.optimizers.connected)
                    },
                    "temperature": {
                        "value": int(inverter.temperature.value),
                        "unit": {
                            "celsius": bool(inverter.temperature.units.celsius),
                            "fahrenheit": bool(inverter.temperature.units.fahrenheit)
                        }
                    },
                    "isolation": {
                        "fault_location": int(inverter.isolation.faultLocation),
                        "r_iso": inverter_isolation_r_iso,
                        "alpha": inverter_isolation_alpha
                    },
                    "subsystem_id": int(inverter.subsystem)
                })
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed