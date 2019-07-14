import solaredge_setapp
import solaredge_setapp.device_manager_pb2


class DeviceManager:
    
    def parse_protobuf(self, bytes):
        
        try:
            proto = solaredge_setapp.device_manager_pb2.DeviceManager()
            proto.ParseFromString(bytes)
        except AttributeError as e:
            print("AttributeError: {e}".format(e=e))

        return {}