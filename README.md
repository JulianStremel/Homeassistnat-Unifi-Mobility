# UniFi Mobility for Home Assistant

A HACS-compatible custom integration that starts Home Assistant support for the official UniFi Mobility API.

The current implementation is intentionally read-only and focused on exposing mobile routing device telemetry as Home Assistant entities. It polls the UniFi cloud Mobility API and creates entities for each discovered Mobility device in the selected workspace.

## Features

- UI-based config flow.
- Cloud polling through `https://api.ui.com/v1/mobility`.
- Device detail polling for each UniFi Mobility device in a workspace.
- Sensors for connection state, WAN source, ISP, LTE signal level, cellular data usage/limit, memory usage, uptime, and client count.
- Diagnostics with API key redaction.

## Installation with HACS

1. Open HACS in Home Assistant.
2. Go to **Integrations**.
3. Open the three-dot menu and choose **Custom repositories**.
4. Add this repository URL and select **Integration** as the category.
5. Install **UniFi Mobility**.
6. Restart Home Assistant.
7. Go to **Settings → Devices & services → Add integration** and search for **UniFi Mobility**.

## Manual installation

1. Copy `custom_components/unifi_mobility` into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & services**.

## Configuration

You need a UniFi API key with Mobility read access. The UniFi Mobility API authenticates with API keys, and the official docs list the cloud base URL as `https://api.ui.com/v1/mobility` with the `X-API-Key` request header.

During setup, enter:

| Field | Description |
| --- | --- |
| API key | UniFi API key with `read:mobility` scope. |
| Base URL | Defaults to `https://api.ui.com/v1/mobility`. Change only for testing or future API routing changes. |
| Workspace ID | Optional. Leave blank to use the first workspace returned by the API. |

## Entities

The integration currently creates the following entities per discovered Mobility device:

- `sensor`: connection state.
- `sensor`: WAN source.
- `sensor`: ISP.
- `sensor`: LTE signal level.
- `sensor`: cellular data usage and limit.
- `sensor`: memory usage.
- `sensor`: uptime.
- `sensor`: connected client count.

Because the public Mobility API is new and payloads may vary by device model and firmware, unsupported or absent fields will appear as unavailable or unknown. The observed device payload does not include GPS coordinates, so this integration does not create device tracker entities.

## Limitations

- Read-only: no Mobility device configuration or management services are implemented.
- Cloud dependency: this integration uses the UniFi cloud API endpoint and requires Home Assistant to reach `api.ui.com`.
- Polling only: data updates on a 60 second interval; webhooks or push updates are not implemented.
- API maturity: the UniFi Mobility API v1.0.0 is new, and response shapes may change or differ between devices.
- Pagination is not yet followed beyond the first response envelope. Large fleets may need additional paging support.
- Workspace selection is basic. If the Workspace ID field is left empty, the first returned workspace is used.
- Entity coverage is intentionally conservative and currently follows the observed device detail payload documented in `docs/knowledgebase.md`.

## Development status

This repository is at the starter integration stage. Useful next steps include:

- Add automated tests with mocked Mobility API responses.
- Add options flow for scan interval and workspace changes.
- Add pagination support for workspace, device, and client list endpoints.
- Add more sensors once additional payload samples confirm stable field names.
- Add translations for more languages.

## API references

- UniFi Mobility API v1.0.0 getting started: <https://developer.ui.com/mobility/v1.0.0/getting-started>
- UniFi Mobility API endpoint overview: <https://developer.ui.com/mobility/v1.0.0>
