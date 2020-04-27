import solaredge_setapp
import solaredge_setapp.information_pb2

import datetime


class Information:

    def parse_protobuf(self, bytes):
        parsed = {}

        try:
            proto = solaredge_setapp.information_pb2.Information()
            proto.ParseFromString(bytes)

            parsed["serial"] = str(proto.sn)
            parsed["cpu"] = str(f"{proto.cpu.major}.{proto.cpu.minor}.{proto.cpu.build}")
            parsed["dsp1"] = str(f"{proto.dsp1.major}.{proto.dsp1.minor}.{proto.dsp1.build}")
            parsed["dsp2"] = str(f"{proto.dsp2.major}.{proto.dsp2.minor}.{proto.dsp2.build}")

            for logger in proto.errors.loggers:
                parsed["errors"] = [{
                    "controller_id": int(logger.controllerID),
                    "subsystem_id": int(logger.subsystem),
                    "error_code": int(error.error_code),
                    "timestamp": int(datetime.datetime.strptime(
                        "{year} {month} {day} {hour} {minutes} {seconds}".format(
                            year=int(error.start_time.year),
                            month=int(error.start_time.month),
                            day=int(error.start_time.day),
                            hour=int(error.start_time.hour),
                            minutes=int(error.start_time.minute),
                            seconds=int(error.start_time.second)
                        ), "%Y %m %d %H %M %S").timestamp()),
                } for error in logger.errors]
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed
