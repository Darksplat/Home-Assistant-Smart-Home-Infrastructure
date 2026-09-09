# Home Assistant Smart Home Infrastructure

Whole-home Home Assistant infrastructure, including dashboards, automations, integrations, ESP/MQTT devices, Thread/Matter, networking, energy, weather, hot water, garden systems, installation guides and troubleshooting documentation.

## Purpose

This repository documents a real residential Home Assistant installation with two goals:

1. preserve reproducible configuration and system knowledge;
2. publish only material that is safe and appropriate for a public repository.

## Live baseline

A sanitized live export was established from the working Home Assistant installation on 9 September 2026.

The source snapshot reported:

- 26 Home Assistant areas
- 163 registry devices before privacy filtering
- 2,688 registry entities before privacy filtering
- 54 integration entries across 41 domains
- 12 storage-mode dashboards before privacy filtering
- 12 custom components
- 3 ESPHome YAML files present on the live host

The public-safety pass intentionally removes household-specific material and complete device/entity registry inventories. Eleven live dashboard exports remain public.

The repeatable export workflow is documented under [`tools/ha-export/`](tools/ha-export/).

## Repository layout

### `home-assistant/`

Public-safe Home Assistant configuration and generated live exports.

The generated baseline is under:

```text
home-assistant/live-export/
```

### `systems/`

Documentation and configuration grouped by functional system, including:

- hot water
- solar and energy
- weather
- FarmBot and garden
- network infrastructure
- Thread and Matter
- security
- garage
- blinds
- waste collection
- household chores
- notifications
- system monitoring

### `inventory/`

Curated and generated public-safe inventory.

- `system-inventory.md` — curated subsystem inventory derived from live evidence
- `generated-live/` — aggregate counts, integration/area/custom-component inventory and safety reports

Complete Home Assistant device/entity registry tables are deliberately not published.

### `docs/`

Whole-system architecture, network, installation, security and troubleshooting documentation.

### `hardware/`

Hardware-specific documentation for hosts, ESP controllers, networking and Thread infrastructure.

### `integrations/`

Installation, configuration and troubleshooting notes for Home Assistant integrations.

### `diagnostics/`

Sanitized diagnostic material suitable for public sharing only.

### `external-projects/`

References to substantial standalone projects that remain authoritative for their specialised hardware/firmware work.

## Live systems represented

The current public baseline includes evidence/configuration for systems such as:

- Fronius solar and Smart Meter
- Sigenergy energy storage
- Amber Electric
- Solcast
- EVOHeat EVO270 hot water
- Ecowitt and Bureau of Meteorology weather
- FarmBot
- Rain Bird irrigation
- Reolink security cameras/NVR/doorbell
- Meross LAN devices and garage door
- Automate Pulse Pro blinds
- Matter / Thread / OTBR
- MQTT / Mosquitto
- Roborock
- Synology DSM
- LG webOS / Yamaha MusicCast / Cast
- Waste Collection Schedule

See [`inventory/system-inventory.md`](inventory/system-inventory.md) for the curated system map.

## Public dashboards

The public live snapshot currently contains:

- Farm Max / garden
- Reolink Security
- Duino-Coin
- Energy Max
- Home Energy
- Home Operations
- Hot Water
- Letterbox Sentinel
- Map
- responsive weather operations centre
- Roller Blinds

The live Household dashboard exists on the source installation but is intentionally excluded from the public repository.

## Security and privacy

This is a public repository.

Never commit passwords, API keys, authentication tokens, private certificates, MQTT/Wi-Fi credentials, Thread datasets, raw authentication stores, MAC addresses, household-member-specific private data or unreviewed diagnostics.

The bulk-export workflow runs an automatic post-export safety scan, but every public diff still requires review.

See [`docs/security/`](docs/security/) for the full policy.

## Related projects

- EVOHeat EVO270 ESP32 / Modbus: https://github.com/Darksplat/EVOHeat-EVO270-ESP32-Modbus
- Home Assistant FarmBot: https://github.com/Darksplat/Homeassistant-Farmbot

## Status

The repository now has a repeatable live baseline rather than an empty documentation skeleton. Work from here is primarily:

- curating subsystem documentation from live evidence
- adding installation/rebuild procedures
- documenting physical network/hardware topology where Home Assistant cannot infer it
- preserving sanitized troubleshooting cases
- refreshing the live snapshot after meaningful Home Assistant changes
