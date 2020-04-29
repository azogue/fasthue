"""Fast-Hue customizer const."""
import voluptuous as vol

from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.helpers import config_validation as cv

DOMAIN = "fasthue"
PLATFORM = "sensor"
UNIQUE_ID = "fast_hue_polling"

SERVICE_SET_UPDATE_INTERVAL = "set_update_interval"

DEFAULT_SENSOR_NAME = "Hue Polling Interval"
DEFAULT_ICON = "mdi:refresh"

# Data schemas
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_SENSOR_NAME): str,
        vol.Required(CONF_SCAN_INTERVAL, default=2): int,
    },
    extra=vol.ALLOW_EXTRA,
)

SET_UPDATE_INTERVAL_SERVICE_SCHEMA = vol.Schema(
    {vol.Required(CONF_SCAN_INTERVAL): vol.All(cv.time_period, cv.positive_timedelta)},
    extra=vol.ALLOW_EXTRA,
)
