"""Fast-Hue customizer sensor for each hue bridge."""
import logging
from datetime import timedelta

from homeassistant.components.hue.bridge import HueBridge
from homeassistant.components.hue.const import DOMAIN as HUE_DOMAIN
from homeassistant.components.hue.sensor_base import SensorManager
from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL, TIME_SECONDS
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr, entity_platform
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DEFAULT_ICON,
    DEFAULT_SENSOR_NAME,
    SERVICE_SET_UPDATE_INTERVAL,
    SET_UPDATE_INTERVAL_SERVICE_SCHEMA,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the component sensors from a config entry."""
    # Register service to change the update interval on specific bridges
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        SERVICE_SET_UPDATE_INTERVAL,
        SET_UPDATE_INTERVAL_SERVICE_SCHEMA,
        "async_set_update_interval",
    )

    # Add one sensor entity for each hue bridge and link it to the hub device
    base_name = config_entry.data.get(CONF_NAME, DEFAULT_SENSOR_NAME)
    initial_scan_interval = max(1, config_entry.data.get(CONF_SCAN_INTERVAL))
    device_registry: dr.DeviceRegistry = await dr.async_get_registry(hass)
    new_entities = []
    for i, (b_entry_id, bridge) in enumerate(hass.data[HUE_DOMAIN].items()):
        # Extract hue hub device to link the sensor with it
        device = next(
            filter(
                lambda dev: dev.via_device_id is None,
                dr.async_entries_for_config_entry(device_registry, b_entry_id),
            )
        )
        new_entities.append(
            HuePollingInterval(
                f"{base_name}_{i + 1}" if i else base_name,
                device,
                bridge.sensor_manager,
                initial_scan_interval,
            )
        )
    async_add_entities(new_entities, False)


class HuePollingInterval(RestoreEntity):
    """
    Class to hold the update_interval of each hue bridge as a sensor.

    Also implementing an entity-service to modify it.

    ** This CC, this entity object, is nothing more than a _hack_ into the
     data update coordinator update interval :) **
    """

    unit_of_measurement = TIME_SECONDS
    icon = DEFAULT_ICON
    should_poll = False
    available = True

    def __init__(
        self,
        name: str,
        device: dr.DeviceEntry,
        sensor_manager: SensorManager,
        scan_interval: int,
    ):
        """Initialize the sensor object."""
        self._name = name
        self._device: dr.DeviceEntry = device
        self._bridge: HueBridge = sensor_manager.bridge
        self._coordinator: DataUpdateCoordinator = sensor_manager.coordinator
        self._custom_scan: timedelta = timedelta(seconds=scan_interval)
        self._default_scan: timedelta = sensor_manager.SCAN_INTERVAL
        self._listener = None

    def _set_new_update_interval(self, scan_interval: timedelta):
        self._custom_scan = scan_interval
        self.async_write_ha_state()
        if self._coordinator.update_interval != self._custom_scan:
            _LOGGER.warning(
                "%s: Modifying the scan_interval from %s to %s",
                self.entity_id,
                self._coordinator.update_interval,
                self._custom_scan,
            )
            self._coordinator.update_interval = self._custom_scan

    async def async_set_update_interval(self, scan_interval):
        """Service call to change the update interval of the hue bridge."""
        self._set_new_update_interval(max(timedelta(seconds=1), scan_interval))

    async def async_will_remove_from_hass(self) -> None:
        """Cancel listeners for sensor updates."""
        if self._listener is not None:
            self._listener()
            self._listener = None
        self._set_new_update_interval(self._default_scan)
        _LOGGER.warning("%s: Removing from HASS", self.entity_id)

    async def async_added_to_hass(self):
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._custom_scan = timedelta(seconds=int(state.state))
            _LOGGER.info(
                "%s: Got update_interval from state restore: %s",
                self.entity_id,
                self._custom_scan,
            )

        # set initial state
        self._set_new_update_interval(self._custom_scan)

        # Set up updates at scan_interval
        @callback
        def _check_polling():
            """Check update_interval on bridge."""
            if self._coordinator.update_interval != self._custom_scan:
                self._set_new_update_interval(self._custom_scan)

        self._listener = self._coordinator.async_add_listener(_check_polling)
        _LOGGER.warning(
            "%s: Added to HASS with update interval: %s",
            self.entity_id,
            self._custom_scan,
        )

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"fast_polling_{self._bridge.config_entry.unique_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return int(self._custom_scan.total_seconds())

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "bridge_host": self._bridge.host,
            "default_polling": self._default_scan.total_seconds(),
        }

    @property
    def device_info(self):
        """Link to the Hue bridge device from the main integration."""
        return {
            "identifiers": self._device.identifiers,
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.model,
            "sw_version": self._device.sw_version,
        }
