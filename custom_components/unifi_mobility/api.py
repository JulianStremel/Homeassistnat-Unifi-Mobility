"""Client for the UniFi Mobility API."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession


class UniFiMobilityApiError(Exception):
    """Base UniFi Mobility API error."""


class UniFiMobilityAuthError(UniFiMobilityApiError):
    """Authentication or authorization failed."""


@dataclass(slots=True)
class UniFiMobilityApiClient:
    """Small async API client for UniFi Mobility."""

    session: ClientSession
    api_key: str
    base_url: str

    async def async_get_workspaces(self) -> list[dict[str, Any]]:
        """Return available workspaces."""
        payload = await self._request("workspaces")
        return _extract_collection(payload)

    async def async_get_devices(self, workspace_id: str) -> list[dict[str, Any]]:
        """Return devices for a workspace."""
        payload = await self._request(f"workspaces/{workspace_id}/devices")
        return _extract_collection(payload)

    async def async_get_device(self, workspace_id: str, device_id: str) -> dict[str, Any]:
        """Return full details for one device."""
        payload = await self._request(f"workspaces/{workspace_id}/devices/{device_id}")
        if isinstance(payload, dict):
            data = payload.get("data")
            if isinstance(data, dict):
                return data
            return payload
        raise UniFiMobilityApiError("Unexpected device response from UniFi Mobility API")

    async def async_get_device_clients(
        self, workspace_id: str, device_id: str
    ) -> list[dict[str, Any]]:
        """Return clients associated with a device."""
        payload = await self._request(f"workspaces/{workspace_id}/devices/{device_id}/clients")
        return _extract_collection(payload)

    async def _request(self, path: str) -> Any:
        """Make a GET request and return the decoded JSON payload."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        headers = {"Accept": "application/json", "X-API-Key": self.api_key}

        try:
            async with asyncio.timeout(30):
                response = await self.session.get(url, headers=headers)
                response.raise_for_status()
                return await response.json()
        except ClientResponseError as err:
            if err.status in (401, 403):
                raise UniFiMobilityAuthError("Invalid UniFi Mobility API key or scope") from err
            raise UniFiMobilityApiError(f"UniFi Mobility API returned HTTP {err.status}") from err
        except (TimeoutError, ClientError) as err:
            raise UniFiMobilityApiError("Unable to connect to UniFi Mobility API") from err


def _extract_collection(payload: Any) -> list[dict[str, Any]]:
    """Extract a list from the envelope formats used by UniFi APIs."""
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        raise UniFiMobilityApiError("Unexpected list response from UniFi Mobility API")

    for key in ("data", "items", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = value.get("items") or value.get("data") or value.get("results")
            if isinstance(nested, list):
                return [item for item in nested if isinstance(item, dict)]

    raise UniFiMobilityApiError("Unable to find a collection in UniFi Mobility API response")
