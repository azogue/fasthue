"""Config flow for Fast-Hue customizer."""
from homeassistant import config_entries

from .const import CONFIG_SCHEMA, DOMAIN, UNIQUE_ID


class ScanIntervalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for `fasthue` to select the polling interval."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

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
