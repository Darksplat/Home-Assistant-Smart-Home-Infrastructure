# Rebuild dependency matrix

This matrix records the minimum system dependencies visible in the sanitized 9 September 2026 Home Assistant baseline.

It is intended for recovery planning. Generated inventories remain the evidence source; this document explains the order and role of the dependencies.

## Core services and apps

| Dependency | Role | Rebuild priority | Notes |
| --- | --- | --- | --- |
| Home Assistant OS / Core | Central platform | Critical | Establish before all other layers |
| Mosquitto broker | MQTT transport | Critical | Required by local MQTT/DIY systems including the deployed EVO270 path |
| Matter Server | Matter controller service | High | Install before recommissioning Matter devices |
| OpenThread Border Router | Thread border-routing service | High | Preserve/rebuild carefully; do not publish operational dataset |
| ESPHome Device Builder | ESP maintenance/build environment | Medium | Raw device YAML/secrets are kept privately |
| Samba share | Read-only/export access from Mac workflow | Medium | Required for `tools/ha-export/run-export.sh` workflow |
| Terminal & SSH | Administration/diagnostics | Medium | Useful for recovery and diagnostics; not a device-control dependency |

## Confirmed custom components

The live export recorded the following custom-component manifests. Versions are a **snapshot**, not a permanent pin; after a rebuild confirm compatibility with the Home Assistant version being installed before updating beyond the known baseline.

| Domain | Component | Snapshot version | Role / subsystem |
| --- | --- | --- | --- |
| `amber_express` | Amber Express | 2.0.1 | Dynamic electricity pricing / solar-control input |
| `aqua_temp` | Aqua Temp | 3.0.37 | Legacy/current hot-water integration evidence; not required for the public read-only EVO270 MQTT firmware path |
| `automate_pulse_pro` | Automate Pulse Pro | 1.0.0 | Roller-blind hub integration |
| `browser_mod` | Browser Mod | 3.2.3 | Frontend/browser services |
| `bureau_of_meteorology` | Bureau of Meteorology | 1.3.5 | Australian weather/forecast data |
| `farmbot` | FarmBot | 0.4.1 | Local FarmBot integration; specialised repo is authoritative |
| `hacs` | HACS | 2.0.5 | Custom integration/frontend package management |
| `meross_cloud` | Meross Cloud IoT | 1.3.12 | Component installed; current generated config-entry inventory does not show an active `meross_cloud` entry |
| `meross_lan` | Meross LAN | 5.8.0 | Local Meross devices, garden switching and garage control |
| `sigen` | Sigenergy ESS | 1.2.7.3 | Sigenergy battery/inverter telemetry |
| `solcast_solar` | Solcast PV Forecast | v4.6.1 | Solar forecast data |
| `waste_collection_schedule` | Waste Collection Schedule | 2.32.0 | Bin schedule sensors |

The generated source for this table is `inventory/generated-live/custom-components.md`.

## Configured integration domains

The sanitized baseline recorded 54 config entries across 41 domains. Important rebuild-facing domains include:

### Infrastructure and protocol

- `mqtt`
- `matter`
- `thread`
- `otbr`
- `bluetooth`
- `hassio`
- `raspberry_pi`
- `rpi_power`
- `upnp`
- `synology_dsm`

### Energy

- `fronius`
- `sigen`
- `amber_express`
- `solcast_solar`
- `co2signal`

### Weather/environment

- `ecowitt`
- `bureau_of_meteorology`
- `met`

### Garden and access

- `farmbot`
- `rainbird`
- `meross_lan`
- `automate_pulse_pro`

### Security/media/appliances

- `reolink`
- `roborock`
- `webostv`
- `yamaha_musiccast`
- `cast`
- `go2rtc`

### Household/platform

- `mobile_app`
- `waste_collection_schedule`
- `browser_mod`
- `google_translate`
- `group`
- `sun`

Use `inventory/generated-live/integrations.md` for the current aggregate source list.

## Dependency order by subsystem

| Subsystem | Must exist first | Then restore/configure | Last validation |
| --- | --- | --- | --- |
| Hot water | LAN, MQTT broker | EVO270 ESP firmware/MQTT discovery | dashboard/entities/fault state |
| Solar & energy | LAN, Fronius/Sigenergy integrations | Amber/Solcast and automation entities | curtailment fail-safe behaviour |
| Weather | LAN | Ecowitt + BOM/forecast integrations | Weather Operations Centre |
| Garden/FarmBot | LAN, weather telemetry, switch integrations | FarmBot + Rain Bird + Meross | pump/zone sequencing and shutdown |
| Blinds | LAN, Automate integration and/or required Matter stack | blind devices | cover position, batteries, schedules |
| Matter/Thread | Matter Server, border router | Thread/Matter commissioning | device control after restart |
| Reolink | LAN/NVR/cameras | Reolink integration/go2rtc path | live streams, detections, chimes |
| Garage | LAN | Meross LAN | state + manual open/close test |
| Letterbox | MQTT and Matter as applicable | Sentinel + parcel sensor | mail/parcel state and alerts |
| Waste collection | Waste Collection Schedule | notification group | tomorrow-bin template and 19:00 reminder |
| Notifications | Companion App registrations | notify group/aliases | test message to intended recipients |
| Duino-Coin | internet/DNS | REST package | account/miner data and dashboard |

## Restore rule

Do not chase dashboard errors until the integration/service below them is healthy. A rebuild should move **bottom-up through dependencies**, not top-down from the UI.
