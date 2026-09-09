# Smart Home System Inventory

This is the curated public-safe inventory for the working Home Assistant installation. It is derived from the generated 9 September 2026 live snapshot, not reconstructed from memory.

The source export reported 26 areas, 163 devices, 2,688 entities, 54 integration entries across 41 domains, 12 storage-mode dashboards and 12 custom components. Detailed device/entity registry rows are intentionally not published.

## Core platform and infrastructure

| System | Live Home Assistant evidence | Role | Repository status |
| --- | --- | --- | --- |
| Home Assistant Core / Supervisor / OS | Home Assistant platform devices plus `hassio`, `raspberry_pi` and `rpi_power` integrations | Central orchestration, UI, automations and integrations | Live baseline exported |
| MQTT | `mqtt` integration and Mosquitto broker app | Local messaging for DIY/local integrations | Live baseline exported |
| Thread / Matter | `thread`, `otbr` and `matter` integrations plus Matter Server / OTBR apps | Thread border routing and Matter device commissioning/control | Live integration evidence present |
| HACS | `hacs` integration and custom-card/custom-integration inventory | Third-party frontend/integration management | Live baseline exported |
| Samba share | Home Assistant Samba app | Read-only/export access from the Mac workflow | Used by `tools/ha-export/` |
| ESPHome | ESPHome Device Builder; 3 YAML filenames detected | ESP-based device management | Filenames only; raw YAML excluded |

## Energy and solar

| System | Live Home Assistant evidence | Role | Dashboard / configuration |
| --- | --- | --- | --- |
| Fronius solar | `fronius` integration; GEN24 and Smart Meter devices | PV generation and grid metering/control | `energy-control-dashboard`, `home-energy`; Amber/Fronius automation exported |
| Sigenergy energy storage | `sigen` integration | Battery, inverter, PV strings and whole-site energy telemetry | `energy-control-dashboard`, `home-energy` |
| Amber Electric | `amber_express` integration | Dynamic import/feed-in pricing and tariff signals | Energy automation uses negative feed-in price logic |
| Solcast | `solcast_solar` integration | PV generation forecasting | Energy dashboards |
| Electricity carbon data | `co2signal` integration | Grid carbon-intensity context | Home/energy entities |

## Hot water

| System | Live Home Assistant evidence | Role | Dashboard / repository |
| --- | --- | --- | --- |
| EVOHeat EVO270 systems | `mqtt` entities plus legacy/current `aqua_temp` integration presence | Two hot-water heat-pump systems with temperature, operating-state, fault and control telemetry | `hot-water` dashboard; specialised project at `Darksplat/EVOHeat-EVO270-ESP32-Modbus` |

The public dashboard contains both hot-water systems but hardware-derived identifiers are aliased by the export safety pass.

## Weather and environment

| System | Live Home Assistant evidence | Role | Dashboard |
| --- | --- | --- | --- |
| Ecowitt | 3 `ecowitt` integration entries; GW3000-series gateway evidence | Local weather-station telemetry | `pioneer-drive-weather-operations-centre-max`, garden dashboard |
| Bureau of Meteorology | `bureau_of_meteorology` custom integration | Australian weather observations/forecast data | Responsive weather operations dashboard |
| Met.no | `met` integration | Additional forecast source | General weather context |
| IKEA air-quality sensor | Matter integration evidence | Local air-quality/environment sensing | Available to HA entities |

## Garden and irrigation

| System | Live Home Assistant evidence | Role | Dashboard / configuration |
| --- | --- | --- | --- |
| FarmBot | `farmbot` integration | Robotic garden automation | `dashboard-garden`; standalone `Darksplat/Homeassistant-Farmbot` project |
| Rain Bird irrigation | `rainbird` integration; ESP-TM2 controller evidence | Garden irrigation zones | Garden dashboard and watering automations |
| Meross outdoor/pump switching | `meross_lan` integration | Pump/power switching used by garden workflows | Garden pressure-pump and watering automations |

## Security, access and monitoring

| System | Live Home Assistant evidence | Role | Dashboard |
| --- | --- | --- | --- |
| Reolink | `reolink` integration; NVR, PoE cameras, doorbell and chimes | CCTV, motion/person/vehicle events and doorbell monitoring | `dashboard-reolink` |
| Letterbox Sentinel | MQTT/DIY entities | Mail/parcel sensing and status | `letterbox-sentinel` dashboard |
| Meross garage door | `meross_lan` integration; garage opener evidence | Garage-door control/status | Home operations / HA cover entities |

## Blinds, Thread and Matter devices

| System | Live Home Assistant evidence | Role | Dashboard |
| --- | --- | --- | --- |
| Automate Pulse Pro | `automate_pulse_pro` integration | Roller-blind hub/control | `roller-blinds` |
| Matter shades and IKEA devices | `matter` integration | Local Matter/Thread plugs, buttons, sensors and shades | Blinds/home operations dashboards |

## Household utilities

| System | Live Home Assistant evidence | Role | Public handling |
| --- | --- | --- | --- |
| Waste Collection Schedule | `waste_collection_schedule` integration | Bin due-date sensors and reminders | Bin-night automation is exported |
| Household chores/NFC | Live package/dashboard exists in source installation | Household task tracking and NFC workflows | Intentionally excluded from public live snapshot because it is member-specific |
| Companion App notifications | 8 `mobile_app` config entries in source | Mobile notifications and presence/device integration | Registry detail excluded; notification services are aliased in public config |

## Media and general smart-home systems

The live integration inventory also confirms:

- LG webOS TV (`webostv`)
- Yamaha MusicCast (`yamaha_musiccast`)
- Roborock (`roborock`)
- Google Cast (`cast`)
- Synology DSM (2 config entries)
- UPnP router monitoring
- Bluetooth
- go2rtc
- Browser Mod

These are part of the working installation but are secondary to the infrastructure-specific subsystem documentation currently being developed.

## Public dashboards in the live baseline

The public export contains 11 dashboard configurations after privacy filtering:

1. Farm Max / garden
2. Reolink Security
3. Duino-Coin
4. Energy Max
5. Home Energy
6. Home Operations
7. Hot Water
8. Letterbox Sentinel
9. Map
10. responsive weather operations centre
11. Roller Blinds

The twelfth source dashboard, Household, is intentionally removed by the public-safety pass.

## Authoritative evidence

Generated evidence lives under `inventory/generated-live/` and `home-assistant/live-export/`. The exporter is repeatable, so this curated inventory should be updated whenever a new public-safe live snapshot materially changes the installed system.
