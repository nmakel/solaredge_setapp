import solaredge_setapp
import solaredge_setapp.power_control_pb2


class PowerControl:
    
    def parse_protobuf(self, bytes):
        
        try:
            proto = solaredge_setapp.power_control_pb2.PowerControl()
            proto.ParseFromString(bytes)
        except AttributeError as e:
            print("AttributeError: {e}".format(e=e))

        return {}