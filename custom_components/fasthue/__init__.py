"""Fast-Hue customizer."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from .const import DOMAIN, PLATFORM, SERVICE_SET_UPDATE_INTERVAL


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up the Fast-Hue component."""
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up the component from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, PLATFORM)
    )

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    hass.services.async_remove(DOMAIN, SERVICE_SET_UPDATE_INTERVAL)
    return await hass.config_entries.async_forward_entry_unload(
        entry, PLATFORM
    )
