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

            parsed["serial"] = str(proto.header.id)
            parsed["timestamp"] = int(proto.header.timestamp)
            parsed["grid_monitor_ms"] = int(proto.grmTime.value)

            parsed["vgrid_max_values"] = [{
                "v": float(value.value.value / value.value.scaling if value.value.scaling != 0 else 1),
                "hold_ms": int(value.holdtime.value)
            } for value in proto.vgMaxList]

            parsed["vgrid_min_values"] = [{
                "v": float(value.value.value / value.value.scaling if value.value.scaling != 0 else 1),
                "hold_ms": int(value.holdtime.value)
            } for value in proto.vgMinList]

            parsed["fgrid_max_values"] = [{
                "hz": float(value.value.value / value.value.scaling if value.value.scaling != 0 else 1),
                "hold_ms": int(value.holdtime.value)
            } for value in proto.fgMaxList]

            parsed["fgrid_min_values"] = [{
                "hz": float(value.value.value / value.value.scaling if value.value.scaling != 0 else 1),
                "hold_ms": int(value.holdtime.value)
            } for value in proto.fgMinList]
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed