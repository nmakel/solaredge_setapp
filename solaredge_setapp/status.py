import solaredge_setapp
import solaredge_setapp.status_pb2


class Status:

    def parse_protobuf(self, bytes):
        parsed = {}

        try:
            proto = solaredge_setapp.status_pb2.Status()
            proto.ParseFromString(bytes)

            parsed = {
                "serial": str(proto.sn),
                "power_ac": float(proto.power_watt),
                "power_ac_limit": int(proto.limit),
                "voltage_ac": float(proto.voltage),
                "frequency": float(proto.frequency_hz),
                "status": int(proto.status),
                "switch": bool(proto.switch_status),
                "cosphi": float(proto.cos_Phi),
                "country_id": int(proto.country),
                "portia_subsystem_id": int(proto.portia_subsystem),
                "afci": {
                    "enabled": bool(proto.afci.enable.value),
                    "manual_reconnect": bool(proto.afci.manual_reconnect.value),
                    "test_result": solaredge_setapp.AfciTestResult(int(proto.afci.test.result)).name
                },
                "optimizers": {
                    "total": int(proto.optimizers_status.enabled),
                    "online": int(proto.optimizers_status.connected)
                },
                "server_connection": bool(proto.s_ok),
                "server_communication": {
                    "physical": solaredge_setapp.CommTestStatus(int(proto.server_comm.lan_test.physical_connection)).name,
                    "ip": solaredge_setapp.CommTestStatus(int(proto.server_comm.lan_test.ip_address)).name,
                    "gateway": solaredge_setapp.CommTestStatus(int(proto.server_comm.lan_test.gateway_link)).name,
                    "internet": solaredge_setapp.CommTestStatus(int(proto.server_comm.lan_test.internet_link)).name,
                    "monitoring": solaredge_setapp.CommTestStatus(int(proto.server_comm.lan_test.monitoring_link)).name,
                    "server": solaredge_setapp.CommTestStatus(int(proto.server_comm.lan_test.s_ok)).name
                },
                "server_channel": {
                    "lan": bool(proto.server_channel.lan.value),
                    "cellular": bool(proto.server_channel.cellular.value),
                    "rs485_1": bool(proto.server_channel.rs485_1_se_slave.value),
                    "rs485_2": bool(proto.server_channel.rs485_2_se_slave.value),
                    "wifi": bool(proto.server_channel.wifi.value),
                    "zigbee": bool(proto.server_channel.zigbee.value)
                },
                "energy": {
                    "day": float(proto.energy.today),
                    "month": float(proto.energy.this_month),
                    "year": float(proto.energy.this_year),
                    "total": float(proto.energy.total)
                },
                "inverters": [],
                "meters": [],
                "batteries": [],
                "communication": {
                    "lan": {
                        "mac": str(proto.communication.lan_info.mac.value),
                        "dhcp": bool(proto.communication.lan_info.dhcp.value),
                        "ip": str(proto.communication.lan_info.ip.ip_address.value),
                        "netmask": str(proto.communication.lan_info.ip.subnet_mask.value),
                        "gateway": str(proto.communication.lan_info.ip.gateway.value),
                        "dns": str(proto.communication.lan_info.ip.dns.value),
                        "connected": bool(proto.communication.lan_info.cable_connected.value)
                    },
                    "rs485_1": {
                        "protocol": {
                            "se_slave": bool(proto.communication.rs485_1.protocol.se_slave),
                            "se_master": bool(proto.communication.rs485_1.protocol.se_master),
                            "modbus_multi_devices": bool(proto.communication.rs485_1.protocol.modbus_multi_devices),
                            "sunspec": bool(proto.communication.rs485_1.protocol.sunspec),
                            "none": bool(proto.communication.rs485_1.protocol.none)
                        }
                    },
                    "rs485_2": {
                        "protocol": {
                            "se_slave": bool(proto.communication.rs485_2.protocol.se_slave),
                            "se_master": bool(proto.communication.rs485_2.protocol.se_master),
                            "modbus_multi_devices": bool(proto.communication.rs485_2.protocol.modbus_multi_devices),
                            "sunspec": bool(proto.communication.rs485_2.protocol.sunspec),
                            "none": bool(proto.communication.rs485_2.protocol.none)
                        }
                    }
                }
            }

            try:
                parsed["status"] = solaredge_setapp.Status(parsed["status"]).name
            except ValueError:
                parsed["status"] = solaredge_setapp.Status(-1).name

            try:
                parsed["country"] = solaredge_setapp.Countries(parsed["country_id"]).name
            except ValueError:
                parsed["country"] = solaredge_setapp.Countries(-1).name

            for inverter in proto.inverters.primary, proto.inverters.left, proto.inverters.right:
                if not inverter.dsp_sn:
                    continue

                if inverter.power.scaling:
                    inverter_power_ac = float(inverter.power.value / inverter.power.scaling)
                else:
                    inverter_power_ac = float(inverter.power.value)

                if inverter.isolation.r_iso.scaling:
                    inverter_isolation_r_iso = float(inverter.isolation.r_iso.value / inverter.isolation.r_iso.scaling)
                else:
                    inverter_isolation_r_iso = float(inverter.isolation.r_iso.value)

                if inverter.isolation.alpha.scaling:
                    inverter_isolation_alpha = float(inverter.isolation.alpha.value / inverter.isolation.alpha.scaling)
                else:
                    inverter_isolation_alpha = float(inverter.isolation.alpha.value)

                parsed["inverters"].append({
                    "serial": str(inverter.dsp_sn),
                    "voltage_dc": float(inverter.voltage),
                    "power_ac": inverter_power_ac,
                    "optimizers": {
                        "total": int(inverter.optimizers_status.enabled),
                        "online": int(inverter.optimizers_status.connected)
                    },
                    "temperature": {
                        "value": int(inverter.temperature.value.value),
                        "unit": {
                            "celsius": bool(inverter.temperature.units.celsius.value),
                            "fahrenheit": bool(inverter.temperature.units.fahrenheit.value)
                        }
                    },
                    "isolation": {
                        "fault_location": int(inverter.isolation.fault_location.value),
                        "r_iso": inverter_isolation_r_iso,
                        "alpha": inverter_isolation_alpha
                    },
                    "subsystem_id": int(inverter.subsystem)
                })
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed
