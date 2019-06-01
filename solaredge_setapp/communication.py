import solaredge_setapp
import solaredge_setapp.communication_pb2


class Communication:

    def parse_protobuf(self, bytes):

        try:
            proto = solaredge_setapp.communication_pb2.Communication()
            proto.ParseFromString(bytes)
        except AttributeError as e:
            print("AttributeError: {e}".format(e=e))

        return {}