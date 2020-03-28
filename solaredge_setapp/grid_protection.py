import solaredge_setapp
import solaredge_setapp.grid_protection_pb2


class GridProtection:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):
        
        parsed = {}

        try:
            proto = solaredge_setapp.grid_protection_pb2.GridProtection()
            proto.ParseFromString(bytes)

            parsed = {
                "grid_monitor_time": proto.grid_monitor_time.value
            }
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed