import solaredge_setapp
import solaredge_setapp.information_pb2

import datetime


class Information:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):

        parsed = {}

        try:
            proto = solaredge_setapp.information_pb2.Information()
            proto.ParseFromString(bytes)

            parsed["serial"] = str(proto.sn)
            parsed["cpu"] = str(f"{proto.cpu.major}.{proto.cpu.minor}.{proto.cpu.build}")
            parsed["dsp1"] = str(f"{proto.dsp1.major}.{proto.dsp1.minor}.{proto.dsp1.build}")
            parsed["dsp2"] = str(f"{proto.dsp2.major}.{proto.dsp2.minor}.{proto.dsp2.build}")

            for logger in proto.errors.loggerList:
                parsed["errors"] = [{
                    "controller_id": int(logger.controllerid), 
                    "subsystem_id": int(logger.subsystem),
                    "error_code": int(error.errorCode),
                    "timestamp": int(datetime.datetime.strptime(
                        "{year} {month} {day} {hour} {minutes} {seconds}".format(
                            year=int(error.startTime.year),
                            month=int(error.startTime.month),
                            day=int(error.startTime.day),
                            hour=int(error.startTime.hour),
                            minutes=int(error.startTime.minute),
                            seconds=int(error.startTime.second)
                        ), "%Y %m %d %H %M %S").timestamp()),
                } for error in logger.errorsList]
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed