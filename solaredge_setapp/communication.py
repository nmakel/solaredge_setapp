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
                    "mac": proto.lan.mac.value,
                    "dhcp": bool(proto.lan.dhcp.value),
                    "ip": proto.lan.ip.ip.value,
                    "netmask": proto.lan.ip.netmask.value,
                    "gateway": proto.lan.ip.gateway.value,
                    "dns": proto.lan.ip.dns.value,
                    "connected": bool(proto.lan.connected.value)
                },
                "modbus_tcp": {
                   "enabled": bool(proto.modbus_tcp.enabled.value)
                },
                "server_connection": bool(proto.server_connection.value),
                "server_channel": {
                      "lan": bool(proto.server_channel.lan.value),
                      "cellular": bool(proto.server_channel.cellular.value),
                      "rs4851": bool(proto.server_channel.rs485_1.value),
                      "rs4852": bool(proto.server_channel.rs485_2.value),
                      "wifi": bool(proto.server_channel.wifi.value),
                      "zigbee": bool(proto.server_channel.zigbee.value) 
                }
            }
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed