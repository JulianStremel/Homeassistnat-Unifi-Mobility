"""Diagnostics support for UniFi Mobility."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_API_KEY, DOMAIN

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    return {
        "entry": {key: ("**REDACTED**" if key in TO_REDACT else value) for key, value in entry.data.items()},
        "device_count": len(coordinator.data.get("devices", {})),
        "client_counts": {
            device_id: len(clients) for device_id, clients in coordinator.data.get("clients", {}).items()
        },
    }
