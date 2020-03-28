import solaredge_setapp
import solaredge_setapp.device_manager_pb2


class DeviceManager:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):
        
        parsed = {}

        try:
            proto = solaredge_setapp.device_manager_pb2.DeviceManager()
            proto.ParseFromString(bytes)

            parsed = {}
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed