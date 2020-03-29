import solaredge_setapp
import solaredge_setapp.power_control_pb2


class PowerControl:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):
        
        parsed = {}

        try:
            proto = solaredge_setapp.power_control_pb2.PowerControl()
            proto.ParseFromString(bytes)
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed