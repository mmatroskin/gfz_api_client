from gfz_client.types import IndexType


# data sources
NOWCAST_LINK = "https://kp.gfz-potsdam.de/app/json/"
FORECAST_LINK = "https://spaceweather.gfz.de/fileadmin/"

FORECAST_KP_PATH = "Kp-Forecast/CSV/kp_product_file_FORECAST_PAGER_SWIFT_LAST.json"
FORECAST_HP3_PATH = "SW-Monitor/hp30_product_file_FORECAST_HP30_SWIFT_DRIVEN_LAST.json"
FORECAST_HP6_PATH = "SW-Monitor/hp60_product_file_FORECAST_HP60_SWIFT_DRIVEN_LAST.json"

# indexes
INDEX_LIST = (
    IndexType.Kp.value,
    "ap",
    "Ap",
    "Cp",
    "C9",
    IndexType.Hp30.value,
    IndexType.Hp60.value,
    "ap30",
    "ap60",
    "SN",
    "Fobs",
    "Fadj"
)
STATE_INDEX_LIST = (IndexType.Kp.value, "ap", "Ap", "Cp", "C9", "SN")
STATE_LIST = ('all', 'def')

# misc
REQUEST_TIMEOUT_SEC = 30
