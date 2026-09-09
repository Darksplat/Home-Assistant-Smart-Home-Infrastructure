# Home Assistant Smart Home Infrastructure

Whole-home Home Assistant infrastructure, including dashboards, automations, integrations, ESP/MQTT devices, Thread/Matter, networking, energy, weather, hot water, garden systems, installation guides and troubleshooting documentation.

## Purpose

This repository documents a real residential Home Assistant installation with two goals:

1. preserve reproducible configuration and system knowledge;
2. publish only material that is safe and appropriate for a public repository.

## Recovery / rebuild

For a Home Assistant host restore, migration or clean rebuild, start here:

- [`docs/installation/README.md`](docs/installation/README.md) — ordered rebuild procedure
- [`docs/installation/DEPENDENCIES.md`](docs/installation/DEPENDENCIES.md) — service/integration dependency matrix
- [`docs/installation/FRONTEND-DEPENDENCIES.md`](docs/installation/FRONTEND-DEPENDENCIES.md) — HACS/Lovelace requirements
- [`docs/installation/PRIVATE-RECOVERY-REQUIREMENTS.md`](docs/installation/PRIVATE-RECOVERY-REQUIREMENTS.md) — what must be kept securely outside the public repo
- [`docs/installation/RECOVERY-CHECKLIST.md`](docs/installation/RECOVERY-CHECKLIST.md) — final post-restore acceptance checklist
- [`docs/troubleshooting/README.md`](docs/troubleshooting/README.md) — whole-system fault isolation

A Home Assistant full backup remains the preferred exact-recovery mechanism. The public repository is deliberately not a copy of credentials, auth state, Thread datasets or private household identity data.

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

The repeatable export workflow is documented under [`tools/ha-export/`](tools/ha-export/). Each refresh now also inventories custom frontend dependencies from the public dashboard exports.

## Repository layout

### `home-assistant/`

Public-safe Home Assistant configuration and generated live exports.

The generated baseline is under:

```text
home-assistant/live-export/
```

### `systems/`

Curated subsystem architecture, operating logic, installation notes and troubleshooting. The current documented set includes:

- [`hot-water/`](systems/hot-water/) — EVOHeat EVO270 local Modbus/MQTT monitoring
- [`solar-energy/`](systems/solar-energy/) — Fronius, Sigenergy, Amber and Solcast
- [`weather/`](systems/weather/) — Ecowitt + Bureau of Meteorology
- [`garden-farmbot/`](systems/garden-farmbot/) — FarmBot, Rain Bird and pump/power control
- [`blinds/`](systems/blinds/) — Automate/Pulse roller blinds
- [`thread-matter/`](systems/thread-matter/) — Thread, OTBR and Matter Server
- [`security/`](systems/security/) — Reolink CCTV/NVR/doorbell/chimes
- [`garage/`](systems/garage/) — Meross LAN garage-door control
- [`letterbox-sentinel/`](systems/letterbox-sentinel/) — DIY MQTT mail/parcel monitoring
- [`waste-collection/`](systems/waste-collection/) — bin sensors and reminders
- [`network/`](systems/network/) — Home Assistant-facing network operations
- [`system-monitoring/`](systems/system-monitoring/) — host/app/integration health
- [`notifications/`](systems/notifications/) — public-safe notification architecture
- [`duino-coin/`](systems/duino-coin/) — REST miner monitoring
- [`household-chores/`](systems/household-chores/) — public design notes; private live implementation excluded

See [`systems/README.md`](systems/README.md) for the subsystem index.

### `inventory/`

Curated and generated public-safe inventory.

- `system-inventory.md` — curated subsystem inventory derived from live evidence
- `generated-live/` — aggregate counts, integration/area/custom-component inventory and safety reports

Complete Home Assistant device/entity registry tables are deliberately not published.

### `docs/`

Whole-system architecture, network, installation/rebuild, security and troubleshooting documentation.

### `hardware/`

Public-safe hardware role/recovery index for hosts, controllers, energy hardware, networking and Thread infrastructure.

### `integrations/`

Integration inventory, custom-component snapshot and rebuild guidance.

### `tools/repo-audit/`

Repository maintenance helpers, including relative Markdown-link checking and dashboard frontend-dependency inventory.

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
- Letterbox Sentinel
- Meross LAN devices and garage door
- Automate Pulse Pro blinds
- Matter / Thread / OTBR
- MQTT / Mosquitto
- Duino-Coin monitoring
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

The repository now contains a sanitized live baseline, curated documentation for the major deployed subsystems, and an ordered rebuild/recovery framework.

Ongoing maintenance is primarily:

- refreshing the live snapshot after meaningful Home Assistant changes;
- keeping the private recovery set current;
- reviewing generated frontend/custom-integration dependencies after updates;
- extending commissioning notes as hardware changes;
- preserving sanitized troubleshooting cases;
- keeping subsystem docs aligned with deployed automations and dashboards.
