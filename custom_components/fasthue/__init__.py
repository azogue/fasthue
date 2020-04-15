"""Fast-Hue customizer."""
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from .const import (
    DEFAULT_SENSOR_NAME,
    DOMAIN,
    PLATFORM,
    SERVICE_SET_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

UI_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_SENSOR_NAME): str,
        vol.Required(CONF_SCAN_INTERVAL, default=2): int,
    },
    extra=vol.ALLOW_EXTRA,
)
CONFIG_SCHEMA = vol.Schema({DOMAIN: UI_CONFIG_SCHEMA}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the component."""
    # logging.warning(f"In manual SETUP with {config}")
    # conf = config.get(DOMAIN)
    # if conf is not None:
    #     logging.warning(f"In manual SETUP with {conf}")
    #     hass.async_create_task(
    #         hass.config_entries.flow.async_init(
    #             DOMAIN, data=conf, context={"source": SOURCE_IMPORT}
    #         )
    #     )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the component from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, PLATFORM)
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.services.async_remove(DOMAIN, SERVICE_SET_UPDATE_INTERVAL)
    return await hass.config_entries.async_forward_entry_unload(
        entry, PLATFORM
    )
