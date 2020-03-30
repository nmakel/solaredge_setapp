import solaredge_setapp
import solaredge_setapp.app_configs_pb2


class WebAppConfigs:
    
    def __init__(self, bytes=False):
        if bytes:
            return self.parse_protobuf(bytes)

    def parse_protobuf(self, bytes):

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

            if proto.mainMenu.countryAndLanguage: parsed["functionality"].append("country_and_language")
            if proto.mainMenu.pairing: parsed["functionality"].append("pairing")
            if proto.mainMenu.communication: parsed["functionality"].append("communication")
            if proto.mainMenu.powerControl: parsed["functionality"].append("power_control")
            if proto.mainMenu.deviceManager: parsed["functionality"].append("device_manager")
            if proto.mainMenu.maintenance: parsed["functionality"].append("maintenance")
            if proto.mainMenu.information: parsed["functionality"].append("information")
            if proto.mainMenu.siteConfiguration: parsed["functionality"].append("site_configuration")
            if proto.mainMenu.status: parsed["functionality"].append("status")
            if proto.mainMenu.gridProtection: parsed["functionality"].append("grid_protection")
        except AttributeError as e:
            print(f"AttributeError: {e}")

        return parsed