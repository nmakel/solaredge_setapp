import solaredge_setapp
import solaredge_setapp.information_pb2


class Information:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):
        
        # str serial
        # str cpu
        # str dsp1
        # str dsp2
        # list loggers [{str controller_id, str subsystem_id}, ...]
    
        try:
            proto = solaredge_setapp.information_pb2.Information()
            proto.ParseFromString(bytes)
            parsed = {}

            parsed["serial"] = str(proto.serial)
            parsed["cpu"] = str(f"{proto.cpu.major}.{proto.cpu.minor}.{proto.cpu.build}")
            parsed["dsp1"] = str(f"{proto.dsp1.major}.{proto.dsp1.minor}.{proto.dsp1.build}")
            parsed["dsp2"] = str(f"{proto.dsp2.major}.{proto.dsp2.minor}.{proto.dsp2.build}")
            parsed["loggers"] = [{
                "controller_id": int(logger.controller_id), 
                "subsystem_id": int(logger.subsystem_id)
            } for logger in proto.loggers.logger]
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed