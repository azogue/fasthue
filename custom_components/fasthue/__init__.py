"""Fast-Hue customizer."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

from .const import DOMAIN, PLATFORM, SERVICE_SET_UPDATE_INTERVAL

_UNDO_UPDATE_LISTENER = "undo_update_listener"


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up the Fast-Hue component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistantType, config_entry: ConfigEntry):
    """Set up the component from a config entry."""
    undo_listener = config_entry.add_update_listener(update_listener)
    hass.data[DOMAIN][config_entry.entry_id] = {
        _UNDO_UPDATE_LISTENER: undo_listener,
    }

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, PLATFORM)
    )

    return True


async def async_unload_entry(hass: HomeAssistantType, config_entry: ConfigEntry):
    """Unload a config entry."""
    hass.services.async_remove(DOMAIN, SERVICE_SET_UPDATE_INTERVAL)
    ok = await hass.config_entries.async_forward_entry_unload(config_entry, PLATFORM)
    hass.data[DOMAIN][config_entry.entry_id][_UNDO_UPDATE_LISTENER]()
    if ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return True


async def update_listener(hass: HomeAssistantType, config_entry: ConfigEntry):
    """Handle options update."""
    original_scan_interval = config_entry.data[CONF_SCAN_INTERVAL]
    new_scan_interval = config_entry.options[CONF_SCAN_INTERVAL]
    if original_scan_interval != new_scan_interval:
        hass.config_entries.async_update_entry(
            config_entry,
            title=config_entry.data[CONF_NAME],
            data={**config_entry.data, **config_entry.options},
            options={},
        )
        hass.async_create_task(hass.config_entries.async_reload(config_entry.entry_id))
