import solaredge_setapp
import solaredge_setapp.grid_protection_pb2


class GridProtection:
    
    def parse_protobuf(self, bytes):
        
        try:
            proto = solaredge_setapp.grid_protection_pb2.GridProtection()
            proto.ParseFromString(bytes)
        except AttributeError as e:
            print("AttributeError: {e}".format(e=e))

        return {}