from gfz_client.types import IndexType, StateType

# data sources
NOWCAST_LINK = "https://kp.gfz-potsdam.de/app/json/"
FORECAST_LINK = "https://spaceweather.gfz.de/fileadmin/"

FORECAST_KP_PATH = "Kp-Forecast/CSV/kp_product_file_FORECAST_PAGER_SWIFT_LAST.json"
FORECAST_HP3_PATH = "SW-Monitor/hp30_product_file_FORECAST_HP30_SWIFT_DRIVEN_LAST.json"
FORECAST_HP6_PATH = "SW-Monitor/hp60_product_file_FORECAST_HP60_SWIFT_DRIVEN_LAST.json"

# indexes
INDEX_LIST = (
    IndexType.Kp,
    IndexType.ap,
    IndexType.Ap,
    IndexType.Cp,
    IndexType.C9,
    IndexType.Hp30,
    IndexType.Hp60,
    IndexType.ap30,
    IndexType.ap60,
    IndexType.SN,
    IndexType.Fobs,
    IndexType.Fadj
)

FORECAST_INDEX_LIST = (
    IndexType.Kp,
    IndexType.Hp30,
    IndexType.Hp60,
)

STATE_INDEX_LIST = (
    IndexType.Kp,
    IndexType.ap,
    IndexType.Ap,
    IndexType.Cp,
    IndexType.C9,
    IndexType.SN
)

STATE_LIST = (StateType.ALL, StateType.DEFINED)

# misc
REQUEST_TIMEOUT_SEC = 15
TEST_DATA = "test_case.json"
