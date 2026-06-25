"""Data update coordinator for UniFi Mobility."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import UniFiMobilityApiClient, UniFiMobilityApiError
from .const import CONF_WORKSPACE_ID, DEFAULT_SCAN_INTERVAL_SECONDS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class UniFiMobilityCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch UniFi Mobility device data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api: UniFiMobilityApiClient,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL_SECONDS),
        )
        self.config_entry = config_entry
        self.api = api
        self.workspace_id = config_entry.data[CONF_WORKSPACE_ID]

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch latest data from the API."""
        try:
            devices = await self.api.async_get_devices(self.workspace_id)
            detailed_devices: dict[str, dict[str, Any]] = {}
            clients: dict[str, list[dict[str, Any]]] = {}
            for device in devices:
                device_id = _first_value(device, "id", "deviceID", "deviceId", "uuid")
                if not device_id:
                    continue
                detailed_devices[device_id] = await self.api.async_get_device(
                    self.workspace_id, device_id
                )
                try:
                    clients[device_id] = await self.api.async_get_device_clients(
                        self.workspace_id, device_id
                    )
                except UniFiMobilityApiError:
                    clients[device_id] = []
            return {"devices": detailed_devices, "clients": clients}
        except UniFiMobilityApiError as err:
            raise UpdateFailed(str(err)) from err


def _first_value(source: dict[str, Any], *keys: str) -> str | None:
    """Return the first non-empty string value for keys."""
    for key in keys:
        value = source.get(key)
        if value is not None:
            return str(value)
    return None
