import solaredge_setapp
import solaredge_setapp.communication_pb2


class Communication:

    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):

        parsed = {}

        try:
            proto = solaredge_setapp.communication_pb2.Communication()
            proto.ParseFromString(bytes)
            
            parsed = {
                "lan": {
                    "mac": str(proto.lan.mac.value),
                    "dhcp": bool(proto.lan.dhcp.value),
                    "ip": str(proto.lan.ip.ipAddress.value),
                    "netmask": str(proto.lan.ip.subnetMask.value),
                    "gateway": str(proto.lan.ip.gateway.value),
                    "dns": str(proto.lan.ip.dns.value),
                    "connected": bool(proto.lan.connected.value)
                },
                "wifi": {
                    "status": int(proto.wifi.status),
                    "wps_duration": int(proto.wifi.wpsDuration.value),
                    "configurations": {
                        "station": bool(proto.wifi.wifiConfigurations.station.value),
                        "wps": bool(proto.wifi.wifiConfigurations.wps.value),
                        "hg": bool(proto.wifi.wifiConfigurations.hg.value)
                    },
                    "external_antenna": bool(proto.wifi.extAntenna.value)
                },
                "modbus_tcp": {
                   "enabled": bool(proto.modbusTcpPort.enabled.value)
                },
                "server_connection": bool(proto.sOk.value),
                "server_channel": {
                    "lan": bool(proto.serverChannel.lan.value),
                    "cellular": bool(proto.serverChannel.cellular.value),
                    "rs485_1": bool(proto.serverChannel.rs4851SeSlave.value),
                    "rs485_2": bool(proto.serverChannel.rs4852SeSlave.value),
                    "wifi": bool(proto.serverChannel.wifi.value),
                    "zigbee": bool(proto.serverChannel.zigbee.value) 
                },
                "rs485_1": {
                    "device_id": int(proto.rs4851.deviceId.value),
                    "protocol": {
                        "se_slave": bool(proto.rs4851.protocol.seSlave.value),
                        "se_master": bool(proto.rs4851.protocol.seMaster.value),
                        "modbus_multi_devices": bool(proto.rs4851.protocol.modbusMultiDevices.value),
                        "sunspec": bool(proto.rs4851.protocol.sunspec.value),
                        "none": bool(proto.rs4851.protocol.none.value)
                    }
                },
                "rs485_2": {
                    "device_id": int(proto.rs4852.deviceId.value),
                    "protocol": {
                        "se_slave": bool(proto.rs4852.protocol.seSlave.value),
                        "se_master": bool(proto.rs4852.protocol.seMaster.value),
                        "modbus_multi_devices": bool(proto.rs4852.protocol.modbusMultiDevices.value),
                        "sunspec": bool(proto.rs4852.protocol.sunspec.value),
                        "none": bool(proto.rs4852.protocol.none.value)
                    }
                },
                "gpio": {
                    "primary": {
                        "disable": bool(proto.gpio.pri.disable.value),
                        "rrcr": bool(proto.gpio.pri.rrcr.value),
                        "ac_relay": bool(proto.gpio.pri.acRelay.value),
                        "rrcr_ac_relay": bool(proto.gpio.pri.rrcrAcRelay.value),
                        "drm": bool(proto.gpio.pri.drm.value),
                        "external_generator": bool(proto.gpio.pri.externalGenerator.value),
                    }
                }
            }

            try: 
                parsed["wifi"]["status"] = solaredge_setapp.WifiStatus(parsed["wifi"]["status"]).name
            except ValueError as e:
                parsed["wifi"]["status"] = solaredge_setapp.WifiStatus(0).name
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed