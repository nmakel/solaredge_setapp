import solaredge_setapp
import solaredge_setapp.region_pb2


class Region:

    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)
    
    def parse_protobuf(self, bytes):
        
        # int country_id
        # str country from enum solaredge_setapp.Countries
        # int language_id
        # str language from enum solaredge_setapp.Languages

        parsed = {}

        try:
            proto = solaredge_setapp.region_pb2.Region()
            proto.ParseFromString(bytes)

            parsed = {
                "country_id": int(proto.country.country),
                "language_id": int(proto.language.language)
            }
            
            try: 
                parsed["country"] = solaredge_setapp.Countries(parsed["country_id"]).name
            except ValueError as e:
                parsed["country"] = solaredge_setapp.Countries(-1).name

            try:
                parsed["language"] = solaredge_setapp.Languages(parsed["language_id"]).name
            except ValueError as e:
                parsed["language"] = solaredge_setapp.Languages(0).name
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed