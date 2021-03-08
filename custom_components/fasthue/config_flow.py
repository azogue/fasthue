"""Config flow for Fast-Hue customizer."""
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import callback

from .const import CONFIG_SCHEMA, DOMAIN, UNIQUE_ID


class ScanIntervalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for `fasthue` to select the polling interval."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get the options flow for this handler to make a tariff change."""
        return FastHueOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(UNIQUE_ID)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=UNIQUE_ID, data=user_input)

        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA)

    async def async_step_import(self, import_info):
        """Handle import from config file."""
        return await self.async_step_user(import_info)


class FastHueOptionsFlowHandler(config_entries.OptionsFlow):
    """
    Handle the Options flow for `fasthue` to edit the configuration.

    **entry.options is used as a container to make changes over entry.data**
    """

    def __init__(self, config_entry):
        """Initialize Fast-Hue options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Manage Hue options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        scan_interval = self.config_entry.data.get(CONF_SCAN_INTERVAL)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, scan_interval
                        ),
                    ): int,
                }
            ),
        )
