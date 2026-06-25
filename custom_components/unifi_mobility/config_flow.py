"""Config flow for UniFi Mobility."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from aiohttp import ClientSession

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import UniFiMobilityApiClient, UniFiMobilityApiError, UniFiMobilityAuthError
from .const import CONF_API_KEY, CONF_BASE_URL, CONF_WORKSPACE_ID, DEFAULT_BASE_URL, DOMAIN


class UniFiMobilityConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a UniFi Mobility config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            session: ClientSession = async_get_clientsession(self.hass)
            api = UniFiMobilityApiClient(
                session=session,
                api_key=user_input[CONF_API_KEY],
                base_url=user_input[CONF_BASE_URL],
            )
            try:
                workspaces = await api.async_get_workspaces()
            except UniFiMobilityAuthError:
                errors["base"] = "invalid_auth"
            except UniFiMobilityApiError:
                errors["base"] = "cannot_connect"
            else:
                workspace_id = user_input.get(CONF_WORKSPACE_ID) or _first_workspace_id(workspaces)
                if not workspace_id:
                    errors["base"] = "no_workspaces"
                else:
                    await self.async_set_unique_id(workspace_id)
                    self._abort_if_unique_id_configured()
                    title = _workspace_title(workspaces, workspace_id)
                    return self.async_create_entry(
                        title=title,
                        data={
                            CONF_API_KEY: user_input[CONF_API_KEY],
                            CONF_BASE_URL: user_input[CONF_BASE_URL].rstrip("/"),
                            CONF_WORKSPACE_ID: workspace_id,
                        },
                    )

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
                vol.Optional(CONF_WORKSPACE_ID): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


def _workspace_id(workspace: dict[str, Any]) -> str | None:
    """Return a workspace identifier from known payload keys."""
    value = (
        workspace.get("workspace_id")
        or workspace.get("id")
        or workspace.get("workspaceID")
        or workspace.get("workspaceId")
    )
    return str(value) if value else None


def _first_workspace_id(workspaces: list[dict[str, Any]]) -> str | None:
    """Return the first workspace identifier."""
    for workspace in workspaces:
        if workspace_id := _workspace_id(workspace):
            return workspace_id
    return None


def _workspace_title(workspaces: list[dict[str, Any]], workspace_id: str) -> str:
    """Return a friendly config entry title."""
    for workspace in workspaces:
        if _workspace_id(workspace) == workspace_id:
            return str(
                workspace.get("workspace_name")
                or workspace.get("name")
                or workspace.get("displayName")
                or "UniFi Mobility"
            )
    return "UniFi Mobility"
