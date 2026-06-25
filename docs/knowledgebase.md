# UniFi Mobility knowledgebase

This file captures API payload shapes that have been observed while developing the Home Assistant integration. Keep examples anonymized and replace real values with placeholders before committing them.

## Workspace collection payload

Source endpoint:

```text
GET /v1/mobility/workspaces
```

Observed response shape:

```json
{
  "err": null,
  "type": "collection",
  "data": [
    {
      "workspace_id": "<workspace-id>",
      "workspace_name": "<workspace-name>",
      "is_owner": "<is-owner>",
      "status": "<workspace-status>"
    }
  ],
  "trace_id": "<trace-id>",
  "offset": "<offset>",
  "limit": "<limit>",
  "total": "<total>"
}
```

## Workspace admins collection payload

Source endpoint:

```text
GET /v1/mobility/workspaces/{workspaceID}/admins
```

Observed response shape:

```json
{
  "err": null,
  "type": "collection",
  "data": [
    {
      "name": "<admin-name>",
      "email": "<admin-email>",
      "status": "<admin-status>",
      "is_owner": "<is-owner>",
      "permissions": {
        "umr": "<umr-permission>"
      }
    }
  ],
  "trace_id": "<trace-id>",
  "offset": "<offset>",
  "limit": "<limit>",
  "total": "<total>"
}
```

## Device collection payload

Source endpoint:

```text
GET /v1/mobility/workspaces/{workspaceID}/devices
```

Observed response shape:

```json
{
  "err": null,
  "type": "collection",
  "data": [
    {
      "id": "<device-id>",
      "name": "<device-name>",
      "model": "<device-model>",
      "state": "<connection-state>",
      "firmware_version": "<firmware-version>",
      "mac_address": "<mac-address>"
    }
  ],
  "offset": "<offset>",
  "limit": "<limit>",
  "total": "<total>"
}
```

## Device detail payload

Source endpoint:

```text
GET /v1/mobility/workspaces/{workspaceID}/devices/{deviceID}
```

Observed response shape:

```json
{
  "err": null,
  "type": "single",
  "data": {
    "id": "<device-id>",
    "name": "<device-name>",
    "model": "<device-model>",
    "state": "<connection-state>",
    "firmware_version": "<firmware-version>",
    "mac_address": "<mac-address>",
    "wan_source": "<wan-source>",
    "wan_ip": "<wan-ip-address>",
    "enabled_wans": [
      "<enabled-wan>"
    ],
    "isp": "<isp-name>",
    "lte_signal_level": "<lte-signal-level>",
    "cellular_data_usage_bytes": "<cellular-data-usage-bytes>",
    "cellular_data_limit_bytes": "<cellular-data-limit-bytes>",
    "memory_usage_percent": "<memory-usage-percent>",
    "uptime_seconds": "<uptime-seconds>",
    "client_count": "<client-count>",
    "host_address": "<host-address>",
    "poe_passthrough": "<poe-passthrough-enabled>",
    "device_mode": "<device-mode>",
    "wifi_enabled": "<wifi-enabled>",
    "wifi_ssid": "<wifi-ssid>",
    "tx_power_level": "<tx-power-level>",
    "vpn_profile_name": "<vpn-profile-name>",
    "vpn_status": "<vpn-status>",
    "firewall_rule_names": [
      "<firewall-rule-name>"
    ],
    "routing_rule_names": [
      "<routing-rule-name>"
    ],
    "ddns_profile_names": [
      "<ddns-profile-name>"
    ],
    "subscription_plan": "<subscription-plan>",
    "subscription_status": "<subscription-status>"
  }
}
```

## Device clients collection payload

Source endpoint:

```text
GET /v1/mobility/workspaces/{workspaceID}/devices/{deviceID}/clients
```

Observed response shape:

```json
{
  "err": null,
  "type": "collection",
  "data": [
    {
      "mac": "<client-mac-address>",
      "name": "<client-name>",
      "type": "<client-connection-type>",
      "connection_status": "<client-connection-status>",
      "ip_address": "<client-ip-address>",
      "is_blocked": "<is-blocked>",
      "wifi_experience": "<wifi-experience>"
    },
    {
      "mac": "<client-mac-address>",
      "name": "<client-name>",
      "type": "<client-connection-type>",
      "connection_status": "<client-connection-status>",
      "ip_address": "<client-ip-address>",
      "is_blocked": "<is-blocked>"
    }
  ],
  "offset": "<offset>",
  "limit": "<limit>",
  "total": "<total>"
}
```

### Notes

- The client payload includes both wireless clients with `wifi_experience` and wired clients without `wifi_experience`.
- The observed device detail payload does not include latitude, longitude, altitude, or speed fields.
- The integration should not create GPS tracker entities from these payloads unless a future API response or endpoint provides verified location fields.
- Current sensor coverage is based on the concrete snake_case fields above instead of guessed camelCase or nested telemetry fields.
