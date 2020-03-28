import solaredge_setapp
import solaredge_setapp.app_configs_pb2


class WebAppConfigs:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):
        
        # int language_id
        # str language from enum solaredge_setapp.Languages
        # list functionality [str, ...]

        parsed = {}

        try:
            proto = solaredge_setapp.app_configs_pb2.WebAppConfigs()
            proto.ParseFromString(bytes)
  
            try:
                parsed["language_id"] = int(proto.language)
                parsed["language"] = solaredge_setapp.Languages(parsed["language_id"]).name
            except ValueError as e:
                parsed["language"] = solaredge_setapp.Languages(0).name

            parsed["functionality"] = []
            if proto.mainmenu.country_and_language: parsed["functionality"].append("country_and_language")
            if proto.mainmenu.pairing: parsed["functionality"].append("pairing")
            if proto.mainmenu.communication: parsed["functionality"].append("communication")
            if proto.mainmenu.power_control: parsed["functionality"].append("power_control")
            if proto.mainmenu.device_manager: parsed["functionality"].append("device_manager")
            if proto.mainmenu.maintenance: parsed["functionality"].append("maintenance")
            if proto.mainmenu.information: parsed["functionality"].append("information")
            if proto.mainmenu.site_configuration: parsed["functionality"].append("site_configuration")
            if proto.mainmenu.status: parsed["functionality"].append("status")
            if proto.mainmenu.grid_protection: parsed["functionality"].append("grid_protection")
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed