import solaredge_setapp
import solaredge_setapp.information_pb2


class Information:
    
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
            parsed["cpu"] = str("{major}.{minor}.{build}".format(
                major=int(proto.cpu.major),
                minor=int(proto.cpu.minor),
                build=int(proto.cpu.build)
            ))
            parsed["dsp1"] = str("{major}.{minor}.{build}".format(
                major=int(proto.dsp1.major),
                minor=int(proto.dsp1.minor),
                build=int(proto.dsp1.build)
            ))
            parsed["dsp2"] = str("{major}.{minor}.{build}".format(
                major=int(proto.dsp2.major),
                minor=int(proto.dsp2.minor),
                build=int(proto.dsp2.build)
            ))
            parsed["loggers"] = [{
                "controller_id": int(logger.controller_id), 
                "subsystem_id": int(logger.subsystem_id)
            } for logger in proto.loggers.logger]
        except AttributeError as e:
            print("AttributeError: {e}".format(e=e))

        return parsed