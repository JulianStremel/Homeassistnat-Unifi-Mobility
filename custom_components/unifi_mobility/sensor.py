"""Sensors for UniFi Mobility."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfInformation, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UniFiMobilityCoordinator


@dataclass(frozen=True, kw_only=True)
class UniFiMobilitySensorEntityDescription(SensorEntityDescription):
    """Describe a UniFi Mobility sensor."""

    value_key: str


SENSOR_DESCRIPTIONS = (
    UniFiMobilitySensorEntityDescription(
        key="state",
        name="State",
        icon="mdi:router-network",
        value_key="state",
    ),
    UniFiMobilitySensorEntityDescription(
        key="wan_source",
        name="WAN source",
        icon="mdi:wan",
        value_key="wan_source",
    ),
    UniFiMobilitySensorEntityDescription(
        key="isp",
        name="ISP",
        icon="mdi:access-point-network",
        value_key="isp",
    ),
    UniFiMobilitySensorEntityDescription(
        key="lte_signal_level",
        name="LTE signal level",
        icon="mdi:signal-cellular-2",
        value_key="lte_signal_level",
    ),
    UniFiMobilitySensorEntityDescription(
        key="cellular_data_usage_bytes",
        name="Cellular data usage",
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        icon="mdi:counter",
        value_key="cellular_data_usage_bytes",
    ),
    UniFiMobilitySensorEntityDescription(
        key="cellular_data_limit_bytes",
        name="Cellular data limit",
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        icon="mdi:database-lock",
        value_key="cellular_data_limit_bytes",
    ),
    UniFiMobilitySensorEntityDescription(
        key="memory_usage_percent",
        name="Memory usage",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:memory",
        value_key="memory_usage_percent",
    ),
    UniFiMobilitySensorEntityDescription(
        key="uptime_seconds",
        name="Uptime",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        suggested_unit_of_measurement=UnitOfTime.MINUTES,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        icon="mdi:timer-outline",
        value_key="uptime_seconds",
    ),
    UniFiMobilitySensorEntityDescription(
        key="client_count",
        name="Clients",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:account-network",
        value_key="client_count",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    coordinator: UniFiMobilityCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = []
    for device_id in coordinator.data["devices"]:
        entities.extend(UniFiMobilitySensor(coordinator, device_id, description) for description in SENSOR_DESCRIPTIONS)
    async_add_entities(entities)


class UniFiMobilitySensor(CoordinatorEntity[UniFiMobilityCoordinator], SensorEntity):
    """UniFi Mobility sensor."""

    entity_description: UniFiMobilitySensorEntityDescription

    def __init__(
        self,
        coordinator: UniFiMobilityCoordinator,
        device_id: str,
        description: UniFiMobilitySensorEntityDescription,
    ) -> None:
        """Initialize a sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def name(self) -> str:
        """Return the entity name."""
        return f"{self._device_name} {self.entity_description.name}"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return _device_info(self._device, self._device_id)

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self._device.get(self.entity_description.value_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return selected device attributes."""
        return {
            "workspace_id": self.coordinator.workspace_id,
            "device_id": self._device_id,
            "model": self._device.get("model"),
            "mac_address": self._device.get("mac_address"),
            "firmware": self._device.get("firmware_version"),
        }

    @property
    def _device(self) -> dict[str, Any]:
        return self.coordinator.data["devices"].get(self._device_id, {})

    @property
    def _device_name(self) -> str:
        return str(self._device.get("name") or self._device_id)


def _device_info(device: dict[str, Any], device_id: str) -> dict[str, Any]:
    """Build Home Assistant device info."""
    return {
        "identifiers": {(DOMAIN, device_id)},
        "name": device.get("name") or device_id,
        "manufacturer": "Ubiquiti",
        "model": device.get("model"),
        "sw_version": device.get("firmware_version"),
    }
