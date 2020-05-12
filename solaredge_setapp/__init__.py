import enum
import itertools

import solaredge_setapp.information
import solaredge_setapp.maintenance
import solaredge_setapp.status


TARGET_VERSION = "1.4.10"


_COUNTRIES = {
    -1: ["Not Set", "COUNTRY_NONE"],
    0: ["General", "COUNTRY_GENERAL"],
    1: ["Australia", "COUNTRY_AUSTRALIA"],
    2: ["France", "COUNTRY_FRANCE"],
    3: ["Germany", "COUNTRY_GERMANY"],
    4: ["Greece (Continent)", "COUNTRY_GREECE_CONTINENT"],
    5: ["Greece (Islands)", "COUNTRY_GREECE_ISLANDS"],
    6: ["Israel", "COUNTRY_ISRAEL"],
    7: ["Italy", "COUNTRY_ITALY"],
    8: ["Spain", "COUNTRY_SPAIN"],
    9: ["United Kingdom", "COUNTRY_UK"],
    10: ["US Auto", "COUNTRY_US_AUTO"],
    11: ["US 208V", "COUNTRY_US_208V"],
    12: ["US 240V", "COUNTRY_US_240V"],
    13: ["US 208V No-Neutral", "COUNTRY_US_208V_NO_NEUTRAL"],
    14: ["US 240V No-Neutral", "COUNTRY_US_240V_NO_NEUTRAL"],
    15: ["Bulgaria", "COUNTRY_BULGARIA"],
    16: ["Czech Republic", "COUNTRY_CZECH_REPUBLIC"],
    17: ["Cyprus", "COUNTRY_CYPRESS"],
    18: ["Belgium", "COUNTRY_BELGIUM"],
    19: ["Netherlands", "COUNTRY_NETHERLANDS"],
    20: ["Portugal", "COUNTRY_PORTUGAL"],
    21: ["Austria", "COUNTRY_AUSTRIA"],
    22: ["Thailand MEA", "COUNTRY_THAILAND_MEA"],
    23: ["Singapore", "COUNTRY_SINGAPORE"],
    24: ["Korea", "COUNTRY_KOREA"],
    25: ["Japan Auto", "COUNTRY_JAPAN_AUTO"],
    26: ["Japan 50Hz", "COUNTRY_JAPAN_50HZ"],
    27: ["Japan 60Hz", "COUNTRY_JAPAN_60HZ"],
    28: ["Taiwan", "COUNTRY_TAIWAN"],
    29: ["Denmark", "COUNTRY_DENMARK"],
    30: ["Sweden", "COUNTRY_SWEDEN"],
    31: ["Thailand PEA", "COUNTRY_THAILAND_PEA"],
    32: ["Sri Lanka", "COUNTRY_SRI_LANKA"],
    33: ["Mauritius", "COUNTRY_MAURITIUS"],
    34: ["Denmark (Residential)", "COUNTRY_DENMARK_RES"],
    35: ["US 277V", "COUNTRY_US_277V"],
    36: ["Slovenia", "COUNTRY_SLOVENIA"],
    37: ["Poland", "COUNTRY_POLAND"],
    38: ["Germany MVGC", "COUNTRY_GERMANY_MVGC"],
    39: ["UK 240V", "COUNTRY_UK_240V"],
    40: ["Lithuania", "COUNTRY_LITHUANIA"],
    41: ["China", "COUNTRY_CHINA"],
    42: ["Philipines", "COUNTRY_PHILIPPINES"],
    43: ["Brazil 220/380V)", "COUNTRY_BRAZIL"],
    44: ["Mexico 220V", "COUNTRY_MEXICO_220"],
    45: ["Mexico 277V", "COUNTRY_MEXICO_277"],
    46: ["Romania", "COUNTRY_ROMANIA"],
    47: ["Latvia", "COUNTRY_LATVIA"],
    48: ["South Africa", "COUNTRY_SOUTH_AFRICA"],
    49: ["Turkey", "COUNTRY_TURKEY"],
    50: ["Italy No SPI", "COUNTRY_ITALY_NO_SPI"],
    51: ["US/Hawaii Auto", "COUNTRY_US_HAWAII_AUTO"],
    52: ["US/Hawaii 208V", "COUNTRY_US_HAWAII_208V"],
    53: ["US/Hawaii 240V", "COUNTRY_US_HAWAII_240V"],
    54: ["US/Hawaii 208V No-Neutral", "COUNTRY_US_HAWAII_208V_NO_NEUTRAL"],
    55: ["US/Hawaii 240V No-Neutral", "COUNTRY_US_HAWAII_240V_NO_NEUTRAL"],
    56: ["US/Hawaii 277V", "COUNTRY_US_HAWAII_277"],
    57: ["Switzerland", "COUNTRY_SWITZERLAND"],
    58: ["Custom", "COUNTRY_CUSTOM"],
    59: ["India", "COUNTRY_INDIA"],
    60: ["Croatia", "COUNTRY_CROATIA"],
    61: ["Jamaica 240V No-Neutral", "COUNTRY_JAMAICA_240_NO_NEUTRAL"],
    62: ["Jamaica 220V No-Neutral", "COUNTRY_JAMAICA_220_NO_NEUTRAL"],
    63: ["Barbados 230V No-Neutral", "COUNTRY_BARBADOS_230_NO_NEUTRAL"],
    64: ["St. Lucia", "COUNTRY_ST_LUCIA"],
    65: ["Australia Queensland", "COUNTRY_AUSTRALIA_QLD"],
    66: ["Denmark VDE", "COUNTRY_DENMARK_VDE"],
    67: ["Denmark VDE (Residential)", "COUNTRY_DENMARK_VDE_RES"],
    68: ["Ireland", "COUNTRY_IRELAND"],
    69: ["US/Kauai Auto", "COUNTRY_US_KAUAI_AUTO"],
    70: ["US/Kauai 208V", "COUNTRY_US_KAUAI_208"],
    71: ["US/Kauai 240V", "COUNTRY_US_KAUAI_240"],
    72: ["US/Kauai 208V No-Neutral", "COUNTRY_US_KAUAI_208_NO_NEUTRAL"],
    73: ["US/Kauai 240V No-Neutral", "COUNTRY_US_KAUAI_240_NO_NEUTRAL"],
    74: ["US/Kauai 277V", "COUNTRY_US_KAUAI_277"],
    75: ["Cyprus 240V", "COUNTRY_CYPRESS_240"],
    76: ["Curacao", "COUNTRY_CURACAO"],
    77: ["Northern Cyprus 240V", "COUNTRY_N_CYPRESS_240"],
    78: ["Israel (Commercial)", "COUNTRY_ISRAEL_COMMERCIAL"],
    79: ["Aruba", "COUNTRY_ARUBA"],
    80: ["Mexico 240V", "COUNTRY_MEXICO_240"],
    81: ["Barbados 115V No-Neutral", "COUNTRY_BARBADOS_115V_NO_NEUTRAL"],
    82: ["Malaysia", "COUNTRY_MALAYSIA"],
    83: ["Tahiti", "COUNTRY_TAHITI"],
    84: ["Hungary", "COUNTRY_HUNGARY"],
    85: ["Kuwait", "COUNTRY_KUWAIT"],
    86: ["Cyprus MV", "COUNTRY_CYPRUS_MV"],
    87: ["Norway", "COUNTRY_NORWAY"],
    88: ["Northern Ireland", "COUNTRY_NORTH_IRELAND"],
    89: ["Germany MV 480V", "COUNTRY_GERMANY_MV_480V"],
    90: ["US/Hawaii2 Auto", "COUNTRY_US_HAWAII2_AUTO"],
    91: ["US/Hawaii2 208V", "COUNTRY_US_HAWAII2_208V"],
    92: ["US/Hawaii2 240V", "COUNTRY_US_HAWAII2_208V_NO_NEUTRAL"],
    93: ["US/Hawaii2 208V No-Neutral", "COUNTRY_US_HAWAII2_240V"],
    94: ["US/Hawaii2 240V No-Neutral", "COUNTRY_US_HAWAII2_240V_NO_NEUTRAL"],
    95: ["US/Hawaii2 277V", "COUNTRY_US_HAWAII2_277"],
    96: ["US/NY Auto", "COUNTRY_US_NY_AUTO"],
    97: ["US/NY 208V", "COUNTRY_US_NY_208V"],
    98: ["US/NY 240V ", "COUNTRY_US_NY_208V_NO_NEUTRAL"],
    99: ["US/NY 208V No-Neutral", "COUNTRY_US_NY_240V"],
    100: ["US/NY 240V No-Neutral", "COUNTRY_US_NY_240V_NO_NEUTRAL"],
    101: ["US/NY 277V ", "COUNTRY_US_NY_277"],
    102: ["Japan MV 420V 50Hz", "COUNTRY_JAPAN_MV_380V_50HZ"],
    103: ["Japan MV 440V 60Hz", "COUNTRY_JAPAN_MV_380V_60HZ"],
    104: ["US/Rule21 Auto", "COUNTRY_US_AUTO_RULE21"],
    105: ["US/Rule21 208V", "COUNTRY_US_208V_RULE21"],
    106: ["US/Rule21 208V No-Neutral", "COUNTRY_US_208V_NO_NEUTRAL_RULE21"],
    107: ["US/Rule21 240V", "COUNTRY_US_240V_RULE21"],
    108: ["US/Rule21 240V No-Neutral", "COUNTRY_US_240V_NO_NEUTRAL_RULE21"],
    109: ["US/Rule21 277V", "COUNTRY_US_277V_RULE21"],
    110: ["Italy 277V No SPI", "COUNTRY_ITALY_277V_NO_SPI"],
    111: ["Philippines 230V Delta", "COUNTRY_PHILIPPINES_230V_DELTA"],
    112: ["UK 480V", "COUNTRY_UK_480V"],
    113: ["Zimbabwe 230V", "COUNTRY_ZIMBABWE_230V"],
    114: ["Indonesia", "COUNTRY_INDONESIA"],
    115: ["Japan MV 480V 50Hz", "COUNTRY_JAPAN_MV_480V_50_HZ"],
    116: ["Japan MV 480V 60Hz", "COUNTRY_JAPAN_MV_480V_60_HZ"],
    117: ["Europe EN50438", "COUNTRY_EUROPE_EN50438"],
    118: ["Cape Verde", "COUNTRY_CAPE_VERDE"],
    119: ["New Zealand", "COUNTRY_NEW_ZEALAND"],
    120: ["Ghana", "COUNTRY_GHANA"],
    121: ["Finland", "COUNTRY_FINLAND"],
    122: ["Grenada", "COUNTRY_GRENADA"],
    123: ["Dubai LV", "COUNTRY_DUBAI_LV"],
    124: ["Slovakia ZSED", "COUNTRY_SLOVAKIA_ZSED"],
    125: ["Slovakia SSED", "COUNTRY_SLOVAKIA_SSED"],
    126: ["Slovakia VSD", "COUNTRY_SLOVAKIA_VSD"],
    127: ["Puerto Rico 277V", "COUNTRY_PUERTO_RICO_277V"],
    128: ["South Africa MV", "COUNTRY_SOUTH_AFRICA_MV"],
    129: ["Philippines MV", "COUNTRY_PHILIPPINES_MV"],
    130: ["Taiwan MV", "COUNTRY_TAIWAN_MV"],
    131: ["India MV", "COUNTRY_INDIA_MV"],
    132: ["US/CO Auto", "COUNTRY_US_CO_AUTO"],
    133: ["US/CO 208V", "COUNTRY_US_CO_208V"],
    134: ["US/CO 208V No-Neutral", "COUNTRY_US_CO_208V_NO_NEUTRAL"],
    135: ["US/CO 240V No-Neutral", "COUNTRY_US_CO_240V_NO_NEUTRAL"],
    136: ["US/CO 240V", "COUNTRY_US_CO_240V"],
    137: ["US/CO 277V", "COUNTRY_US_CO_277V"],
    138: ["Australia Victoria", "COUNTRY_VICTORIA"],
    139: ["Kenya", "COUNTRY_KENYA"],
    140: ["Turkey MV", "COUNTRY_TURKEY_MV"],
    141: ["Spain MV", "COUNTRY_SPAIN_MV"],
    142: ["Thailand MEA MV", "COUNTRY_THAILAND_MEA_MV"],
    143: ["Thailand PEA MV", "COUNTRY_THAILAND_PEA_MV"],
    144: ["China MV", "COUNTRY_CHINA_MV"],
    145: ["Taiwan 220V No-Neutral", "COUNTRY_TAIWAN_220_NO_NEUTRAL"],
    146: ["Mauritius >220K", "COUNTRY_MAURITIUS_ABOVE_220K"],
    147: ["France MV", "COUNTRY_FRANCE_MV"],
    148: ["Czech Republic 16A", "COUNTRY_CEZ"],
    149: ["Belgium Delta", "COUNTRY_BELGIUM_DELTA"],
    150: ["Norway Delta", "COUNTRY_NORWAY_DELTA"],
    151: ["Netherlands MV", "COUNTRY_NETHERLANDS_MV"],
    152: ["Macau", "COUNTRY_MACAU"],
    153: ["Argentina", "COUNTRY_ARGENTINA"],
    154: ["Argentina (Commercial)", "COUNTRY_ARGENTINA_COMMERCIAL"],
    155: ["Sweden MV", "COUNTRY_SWEDEN_MV"],
    156: ["Vietnam", "COUNTRY_VIETNAM"],
    157: ["Brazil 127/220V", "COUNTRY_BRAZIL_127V_220V"],
    158: ["Barbados 220V", "COUNTRY_BARBADOS_200"],
    159: ["ISO-NE 208V", "COUNTRY_US_NEW_ENGLAND_208"],
    160: ["ISO-NE 240V", "COUNTRY_US_NEW_ENGLAND_240"],
    161: ["ISO-NE 208V No-Neutral", "COUNTRY_US_NEW_ENGLAND_208_NO_NEUTRAL"],
    162: ["ISO-NE 240V No-Neutral", "COUNTRY_US_NEW_ENGLAND_240_NO_NEUTRAL"],
    163: ["ISO-NE 277V", "COUNTRY_US_NEW_ENGLAND_277"],
    164: ["Korea Low DC", "COUNTRY_KOREA_LOW_DC"],
    165: ["Israel 480 MV", "COUNTRY_ISRAEL_480V_MV"],
    166: ["Brazil 277/480V", "COUNTRY_BRAZIL_277"],
    167: ["Hungary EON", "COUNTRY_HUNGARY_EON"],
    168: ["Spain (Islands)", "COUNTRY_SPANISH_ISLANDS"],
    169: ["Peru", "COUNTRY_PERU"],
    170: ["Columbia", "COUNTRY_COLUMBIA"],
    171: ["Chile", "COUNTRY_CHILE"],
    172: ["Ecuador", "COUNTRY_ECUADOR"],
    173: ["Qatar", "COUNTRY_QATAR"],
    174: ["Australia 480V", "COUNTRY_AUSTRALIA_480V"],
    175: ["Hong Kong", "COUNTRY_HONG_KONG"],
    176: ["Uruguay", "COUNTRY_URUGUAY"],
    177: ["Italy A68", "COUNTRY_ITALIY_A68"],
    178: ["Estonia", "COUNTRY_ESTONIA"],
    179: ["Mauritius 2", "COUNTRY_MAURITIUS_2"],
    180: ["Surinam", "COUNTRY_SURINAM"],
    181: ["Western Power", "COUNTRY_WESTERN_POWER"],
    182: ["India (Kerala)", "COUNTRY_INDIA_KERALA"]
}
Countries = enum.Enum(
    value="Countries",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _COUNTRIES.items()
    )
)


_STATUS = {
    -1: ["Not Set", "UNSET"],
    0: ["Shutting Down", "SHUTTING_DOWN"],
    1: ["Error", "ERROR"],
    2: ["Standby", "STANDBY"],
    3: ["Pairing", "PAIRING"],
    4: ["Producing", "POWER_PRODUCTION"],
    5: ["AC Charging", "AC_CHARGING"],
    6: ["Not Paired", "NOT_PAIRED"],
    7: ["Night Mode", "NIGHT_MODE"],
    8: ["Grid Monitoring", "GRID_MONITORING"],
    9: ["Idle", "IDLE"],
    10: ["Grid Pairing", "GRM_PAIRING"],
    11: ["PID Rectification", "PID_RECTIFICATION"]
}
Status = enum.Enum(
    value="Status",
    names=itertools.chain.from_iterable(
        itertools.product(v, [k]) for k, v in _STATUS.items()
    )
)


class AfciTestResult(enum.Enum):
    AFCI_TEST_FAIL = 0
    AFCI_TEST_ERROR = -1
    AFCI_TEST_PASS = 1


class InverterTestCondition(enum.Enum):
    TEST_COND_OK = 0
    TEST_COND_NOT_READY_GRM = 1
    TEST_COND_NOT_READY_PROD = 2
    TEST_COND_NOT_READY_INV_OFF = 3


class InverterTestStatus(enum.Enum):
    TEST_STATUS_NOT_TESTED = 0
    TEST_STATUS_PASSED = 1
    TEST_STATUS_FAILED = 2


class BatterySelfTestPrecondition(enum.Enum):
    TEST_PRE_COND_OK = 0
    TEST_PRE_COND_NOT_READY_INV_OFF = 1
    TEST_PRE_COND_NOT_READY_INV_COMM_ERROR = 2
    TEST_PRE_COND_NOT_READY_INV_BATT_ERROR = 3
    TEST_PRE_COND_NOT_READY_MIN_SOE = 4


class BatterTestStatus(enum.Enum):
    NOT_TESTED = 0
    IN_PROGRESS = 1
    PASSED = 2
    FAILED = 3


class LanStatus(enum.Enum):
    OK = 0


class CellularSignal(enum.Enum):
    NONE = 0
    LOW = 1
    LOWEST = 2
    MEDIUM = 3
    HIGH = 4
    HIGHEST = 5
    UNKNOWN = 6


class WifiSignal(enum.Enum):
    NONE = 0
    LOW = 1
    MID = 2
    HIGH = 3
    EXCELLENT = 4


class ZigbeeSignal(enum.Enum):
    NONE = 0
    LOW = 1
    MID = 2
    HIGH = 3


class ZigbeeSlaveStatus(enum.Enum):
    NOT_CONNECTED = 0
    CONNECTED = 1
    MASTER_NOT_FOUND = 2


class ZigbeeModuleStatus(enum.Enum):
    INITIALIZING = 0
    OK = 1


class EvseCarStatus(enum.Enum):
    disconnected = 0
    connected = 1
    charging_car = 2


class EvseChargerStatus(enum.Enum):
    ready = 0
    initializing = 1
    charging = 2
    charging_boost = 3
    charging_excess_pv = 4


class MeterConnectionType(enum.Enum):
    RS485_1 = 0
    RS485_2 = 1
    S0 = 2


class MeterStatus(enum.Enum):
    OK = 0
    COMM_ERROR = 1


class BatteryStatus(enum.Enum):
    CONNECTED = 0
    DISCNNECTED = 1


class BatteryState(enum.Enum):
    BMS_STATE_INVALID = 0
    BMS_STATE_OFF = 1
    BMS_STATE_STDBY = 2
    BMS_STATE_INIT = 3
    BMS_STATE_CHARGE = 4
    BMS_STATE_DISCHARGE = 5
    BMS_STATE_FAULT = 6
    BMS_STATE_IDLE = 7
    BMS_STATE_COMM_ERROR = 8
    BMS_STATE_RESERVED1 = 9
    BMS_STATE_RESERVED2 = 10
    BMS_STATE_SLEEP = 11


class HeaderType(enum.Enum):
    ERROR = 0
    WARNING = 1
    INFORMATION = 2


class PairingStatusInfo(enum.Enum):
    OK = 0
    INV_OFF = 2
    NIGHT_MODE = 3
    IN_PROCESS = 4
    ERROR = 5
    ERROR_OPT_DETECT = 6
    ERROR_STRING_DETECT = 7
    NOT_IN_PROCESS = 8


class PairingStatusStage(enum.Enum):
    NOT_ACTIVE = 0
    WAIT_VIN_DECREASE = 1
    PAIRING = 2
    SAVE_SESSION = 3
    OPT_DETECT = 4
    STRING_DETECT = 5
    END = 6


class CommTestStatus(enum.Enum):
    FAILED = 0
    PASSED = 1
    NOT_TESTED = 2


class ServerChannelMethod(enum.Enum):
    MANUAL_SELECT = 0
    AUTO_SELECT = 1


class OperationMode(enum.Enum):
    INV_OPER_MODE_ON_GRID = 0
    INV_OPER_MODE_STORAGE_OFF_GRID = 1
    INV_OPER_MODE_DG_OFF_GRID = 2


class LanNetStatus(enum.Enum):
    LAN_UNKNOWN = 0
    LAN_CABLE_NOT_CONNECTED = 1
    LAN_ERROR_DHCP = 2
    LAN_NO_INTERNET_CONNECTION = 3
    LAN_ERROR_DNS = 4
    LAN_CONNECTING_TO_SERVER = 5
    LAN_WAITING_FOR_SERVER_RESPONSE = 6
    LAN_SERVER_RESPONDED = 7


class WifiNetStatus(enum.Enum):
    WIFI_UNKNOWN = 0
    WIFI_NOT_CONNECTED = 1
    WIFI_CONNECTION_IN_PROGRESS = 2
    WIFI_ERROR_WRONG_PASSWORD = 3
    WIFI_ERROR_UNREACHABLE = 4
    WIFI_ERROR_DHCP = 5
    WIFI_ERROR_CONNECTION_OTHER = 6
    WIFI_NO_INTERNET_CONNECTION = 7
    WIFI_ERROR_DNS = 8
    WIFI_CONNECTING_TO_SERVER = 9
    WIFI_WAITING_FOR_SERVER_RESPONSE = 10
    WIFI_SERVER_RESPONDED = 11


class RS485SlaveNetStatus(enum.Enum):
    RS485_SLAVE_UNKNOWN = 0
    RS485_SLAVE_NOT_CONFIGURED = 1
    RS485_SLAVE_NO_MASTER = 2
    RS485_SLAVE_NO_GRANT_RECEIVED = 3
    RS485_SLAVE_CONNECTED_TO_MASTER = 4
    RS485_SLAVE_SERVER_RESPONDED = 5


class ZigbeeSlaveNetStatus(enum.Enum):
    ZB_SLAVE_UNKNOWN = 0
    ZB_SLAVE_NOT_DETECTED = 1
    ZB_DETECTION_IN_PROGRESS = 2
    ZB_INIT_MODULE = 3
    ZB_SLAVE_NOT_CONFIGURED = 4
    ZB_SLAVE_DISASSOCIATED = 5
    ZB_SLAVE_NO_COMM_WITH_COORDINATOR = 6
    ZB_SLAVE_CONNECTED_TO_COORDINATOR = 7
    ZB_SLAVE_SERVER_RESPONDED = 8


class CellNetStatus(enum.Enum):
    CELL_UNKNOWN = 0
    CELL_NOT_DETECTED = 1
    CELL_DETECTION_IN_PROGRESS = 2
    CELL_INIT_MODULE = 3
    CELL_NO_SIM_CARD = 4
    CELL_MISSING_PIN = 5
    CELL_SIM_NOT_REGISTERED = 6
    CELL_MODEM_NOT_ACTIVATED = 7
    CELL_MISSING_APN = 8
    CELL_NO_SIGNAL = 9
    CELL_NO_COMM_WITH_MODULE = 10
    CELL_ESTABLISHING_INTERNET_CONNECTION = 11
    CELL_NO_INTERNET_CONNECTION = 12
    CELL_NO_TELEM_PLAN_SELECT = 13
    CELL_ACTIVATING_TELEM_PLAN = 14
    CELL_ACTIVATING_ERROR_NO_RESPONSE = 15
    CELL_ACTIVATING_ERROR_UNIDENTIFIED_NUMBER = 16
    CELL_ACTIVATING_ERROR_SMS_BLOCKED = 17
    CELL_ACTIVATING_ERROR_NO_SMS = 18
    CELL_ACTIVATING_ERROR = 19
    CELL_CONNECTING_TO_SERVER = 20
    CELL_CONNECTED = 21
    CELL_SERVER_RESPONDED = 22


class ControllerTypes(enum.Enum):
    ORTIA = 0
    VENUS_DSP1 = 1
    VENUS_DSP2 = 2
    JUPITER_DSP1 = 3
    JUPITER_DSP2 = 4
    VEGA_DSP = 5
    DISP_CTRL = 6
    FAN_CTRL = 7
    VENUS3_DSP1 = 8
    VENUS3_DSP2 = 9
    VENUS_LITE_DSP1 = 10
    VENUS_LITE_DSP2 = 11
    JUPITER_DSP1_BOOTLOADER = 12
    EVSE = 13
    SE_DCDC = 14
    METER = 15
    LG_DCDC = 16
    LG_BMS = 17
    HG2 = 18
    JUPITER_SE_DSP1 = 19
    JUPITER_SE_DSP2 = 20
    BUI = 21
    FOUR_BOX = 22
    VENUS3_SE_DSP1 = 23
    VENUS3_SE_DSP2 = 24


class ProductTypes(enum.Enum):
    VENUS = 0
    JUPITER = 1
    VEGA = 2
    CCG = 3
    GEMINI = 4
    SATURN = 5
    MARS = 6
    VOYAGER = 7
    VENUS3 = 8
    JUMBO_JUPITER = 9
    VENUS_LITE = 10
    CCG_UNUSED = 11
    FFG = 12
    ZIGBEE_GATEWAY = 13
    EVSE_SA = 14
    WIFI_REPEATER = 15
    WIFI_GATEWAY = 16
    PRODUCT_TYPE_WATER_HEATER = 17
    PRODUCT_TYPE_CCG_GPU = 18
    PRODUCT_TYPE_METER = 19
    PRODUCT_TYPE_JJ_4BOX = 20
    PRODUCT_TYPE_BUI = 21
    PRODUCT_TYPE_NONE = 22


class UnitPosition(enum.Enum):
    UNKNOWN = 0
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    PRIMARY = 4
