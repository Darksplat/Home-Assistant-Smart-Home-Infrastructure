# Hardware

This directory is the public-safe physical-infrastructure index for the Home Assistant installation.

The repository documents hardware by **role, model/protocol where useful, and recovery dependency**. Stable hardware identifiers, private addresses, credentials and unnecessary serial numbers are intentionally omitted.

## Core platform

| Hardware / service | Role | Recovery note |
| --- | --- | --- |
| Raspberry Pi Home Assistant host | Runs Home Assistant OS/Core and apps | Keep current full backups and proven boot/recovery media available |
| Home LAN/router/switching | Connectivity for local integrations | Private addressing/reservations belong in the private recovery record |
| Synology NAS infrastructure | Monitored storage/services | Credentials and management addressing remain private |

## Local automation/controllers

| Hardware | Role | Public documentation |
| --- | --- | --- |
| Waveshare ESP32-S3-RS485-CAN controllers | Local EVOHeat EVO270 RS485/Modbus-to-MQTT monitoring | `systems/hot-water/` and standalone `Darksplat/EVOHeat-EVO270-ESP32-Modbus` |
| ESPHome-managed devices | Local ESP automation/sensing | Public export records filenames only; raw YAML/secrets are private recovery material |
| FarmBot controller/platform | Garden robotics | `systems/garden-farmbot/` and standalone `Darksplat/Homeassistant-Farmbot` |

## Energy hardware

| Hardware | Role | Documentation |
| --- | --- | --- |
| Fronius GEN24 system / meter path | PV generation, metering and local curtailment control | `systems/solar-energy/` |
| Sigenergy energy-storage system | Battery/inverter/PV/whole-site telemetry | `systems/solar-energy/` |

The public repository documents control behaviour but not private network addressing or vendor-account credentials.

## Weather and garden hardware

| Hardware | Role | Documentation |
| --- | --- | --- |
| Ecowitt weather station/gateway | Local temperature, humidity, wind, rain, UV and solar-radiation telemetry | `systems/weather/` |
| Rain Bird irrigation controller | Garden-zone switching | `systems/garden-farmbot/` |
| Meross outdoor/power devices | FarmBot/pump power and other LAN switching | `systems/garden-farmbot/`, `systems/garage/` |

## Security/access hardware

| Hardware | Role | Documentation |
| --- | --- | --- |
| Reolink NVR, cameras and doorbell | CCTV, live streams, detection and doorbell monitoring | `systems/security/` |
| Reolink chimes | Doorbell/chime functions | `systems/security/` |
| Meross garage-door device | Garage cover state/control | `systems/garage/` |
| Letterbox Sentinel hardware | Mail sensing, environment and battery telemetry | `systems/letterbox-sentinel/` |
| Parcel sensor | Parcel-door sensing via Matter/Thread path | `systems/letterbox-sentinel/`, `systems/thread-matter/` |

## Blinds / Thread / Matter

| Hardware | Role | Documentation |
| --- | --- | --- |
| Automate Pulse Pro hub | Deployed roller-blind integration path | `systems/blinds/` |
| Matter/Thread devices | Local shades/plugs/buttons/sensors as commissioned | `systems/thread-matter/` |
| Thread border-router infrastructure | IPv6 mesh-to-LAN bridge for Thread devices | `systems/thread-matter/` |

Thread datasets, setup codes and stable radio identifiers are private recovery material and must not be committed.

## Hardware replacement rule

When replacing a controller, gateway or host:

1. record the old device's role before removal;
2. confirm the replacement's power/network/protocol path independently;
3. commission it at the integration layer before changing dashboards;
4. expect entity IDs or device identities to change;
5. update subsystem documentation when architecture changes;
6. refresh the sanitized live export only after the new hardware is stable.

## Private hardware record

Maintain a separate private record for information that is operationally useful but unsuitable for public GitHub, such as:

- exact management addresses and DHCP reservations;
- Wi-Fi credentials;
- MAC addresses;
- serial numbers needed for warranty/support;
- setup/commissioning codes;
- physical switch-port mapping where it reveals unnecessary household detail.

See `docs/installation/PRIVATE-RECOVERY-REQUIREMENTS.md` for the recovery checklist.
