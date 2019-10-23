import solaredge_setapp
import solaredge_setapp.communication_pb2


class Communication:

    def parse_protobuf(self, bytes):

        try:
            proto = solaredge_setapp.communication_pb2.Communication()
            proto.ParseFromString(bytes)
            parsed = {
                "lan": {
                    "mac": proto.lan.mac,
                    "dhcp": bool(proto.lan.dhcp.value),
                    "ip": proto.lan.ip.ip.value,
                    "netmask": proto.lan.ip.subnetmask.value,
                    "gateway": proto.lan.ip.gateway.value,
                    "dns": proto.lan.ip.dns.value
                },
                "modbus_tcp": {
                   "enabled": bool(proto.modbus_tcp.enabled.value)
                }
            }
        except AttributeError as e:
            print("AttributeError: {e}".format(e=e))

        return parsed