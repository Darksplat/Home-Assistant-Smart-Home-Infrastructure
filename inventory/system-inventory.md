# Smart Home System Inventory

This is the initial public-safe inventory of the known Home Assistant installation and supporting smart-home infrastructure.

It is intentionally a **working inventory**, not yet a complete export of the live system. Each subsystem will be verified against the current Home Assistant installation as its configuration is migrated into this repository.

## Core Home Assistant infrastructure

| System | Hardware / platform | Role | Status | Notes |
|---|---|---|---|---|
| Primary Home Assistant host | Raspberry Pi 400 | Runs the main Home Assistant installation | Deployed | Connected through both Ethernet and Wi-Fi. Exact live addressing is intentionally omitted from this public inventory. |
| Dedicated Thread host | Raspberry Pi, hostname `ha-thread` | Dedicated Thread / OTBR infrastructure host | Deployed | Ethernet-connected Linux host with a Thread `wpan0` interface. Docker is also present. |
| GitHub configuration repository | `Darksplat/Home-Assistant-Smart-Home-Infrastructure` | Public-safe source of documentation, dashboards, automations and reproducible configuration | Deployed | This repository. |

## Network infrastructure

| Device / system | Model / type | Role | Status | Notes |
|---|---|---|---|---|
| Main router | ASUS GT-AX11000 | Primary router, Wi-Fi and network gateway | Deployed | Has been the focus of intermittent WAN/IP-loss troubleshooting. |
| AiMesh nodes | ASUS AiMesh nodes ×2 | Wireless mesh coverage | Deployed | Garage and shed locations are known operationally; exact node-to-location mapping still needs verification in the public documentation. |
| Managed/smart switch | TP-Link TL-SG1024DE | Main Ethernet switching infrastructure | Deployed | Management interface available locally. |
| Network video recorder | Reolink 16-channel NVR | Camera recording and security infrastructure | Deployed | Home Assistant relationship to be documented in the security subsystem. |
| Alarm system | Bosch 6000 | Intrusion/security system | Deployed | Integration path and current HA entities still require inventory. |
| Roller-blind hub | Automate Pulse / RA Pulse hub | Roller blind control and Thread-related infrastructure | Deployed | Home Assistant integration currently uses Automate/Pulse components. |

## Hot-water systems

| System | Hardware | HA path | Status | Notes |
|---|---|---|---|---|
| EVOHeat hot-water unit 1 | EVOHeat EVO270 + Waveshare ESP32-S3-RS485-CAN | Local RS485/Modbus → ESP32 → MQTT → Home Assistant | Field tested | Dedicated standalone repository contains the detailed protocol, firmware and dashboard work. |
| EVOHeat hot-water unit 2 | EVOHeat EVO270 + Waveshare ESP32-S3-RS485-CAN | Local RS485/Modbus → ESP32 → MQTT → Home Assistant | Field tested | Same architecture as unit 1. |
| Legacy Aqua Temp integration | Original/legacy cloud or custom integration | Home Assistant custom/cloud integration | Legacy | Retained only where needed for migration/history; local ESP32/MQTT monitoring is preferred. |

Related project: [EVOHeat-EVO270-ESP32-Modbus](https://github.com/Darksplat/EVOHeat-EVO270-ESP32-Modbus)

## Solar and energy

| System | Hardware / service | HA path | Status | Notes |
|---|---|---|---|---|
| Fronius solar inverter | Fronius Symo GEN24 10.0 kW, three-phase | Home Assistant Fronius entities / local inverter control | Deployed | HA control testing has successfully limited inverter AC output. |
| Sigenergy system | Sigenergy inverter/battery platform | Home Assistant Sigenergy integration | Deployed | Solar/energy relationship with Fronius and Amber still needs full architecture documentation. |
| Amber Electric | Energy retailer / dynamic pricing and curtailment | Home Assistant Amber integration | Deployed | Curtailment behaviour is being documented, including Fronius versus Sigenergy response. |
| Solcast | Solar forecasting service | Home Assistant integration | Deployed | Entity and dashboard inventory still required. |

## Weather

| System | Hardware / service | HA path | Status | Notes |
|---|---|---|---|---|
| Local weather station | Ecowitt WS90 with GW3000 gateway | Ecowitt → Home Assistant | Deployed | Primary source for local outdoor measurements. |
| Bureau of Meteorology | Australian BOM integration | BOM → Home Assistant | Deployed | Used alongside local Ecowitt data. |
| Weather dashboard | Home Assistant Lovelace | Ecowitt + BOM entities | Partial | Desktop dashboard exists; responsive mobile/iPad work has been undertaken and will be migrated here. |

## Garden and FarmBot

| System | Hardware / service | HA path | Status | Notes |
|---|---|---|---|---|
| FarmBot | FarmBot Genesis | Home Assistant custom integration / API | Deployed | Includes automations, dashboard work and graceful-shutdown logic. |
| Garden weather data | Ecowitt/BOM | Shared Home Assistant entities | Deployed | Used by garden/FarmBot dashboards. |

Related project: [Homeassistant-Farmbot](https://github.com/Darksplat/Homeassistant-Farmbot)

## Garage

| System | Hardware / service | HA path | Status | Notes |
|---|---|---|---|---|
| Garage door | Meross garage-door opener | Meross → Home Assistant cover entity | Deployed | A prior outage produced an `unavailable` HA entity while the Meross app continued to work, confirming a HA/integration-side connectivity fault rather than local actuator failure. |

## Blinds / Thread

| System | Hardware / service | HA path | Status | Notes |
|---|---|---|---|---|
| Roller blinds | Automate Pulse ecosystem | Automate/Pulse → Home Assistant | Deployed | Hub and Thread-related architecture to be documented. |
| Thread infrastructure | Dedicated `ha-thread` host plus Thread radio/interface | OTBR / Thread | Deployed | Full topology, border-router role and commissioning procedure still to be documented. |

## Security

| System | Hardware / service | HA path | Status | Notes |
|---|---|---|---|---|
| CCTV | Reolink 16-channel NVR | Reolink → Home Assistant | Deployed | Entity and camera inventory still required. |
| Alarm | Bosch 6000 | Home Assistant integration path to verify | Partial | Hardware is deployed; HA integration details need a current system audit. |

## Waste collection

| System | HA entities / service | Status | Notes |
|---|---|---|---|
| Waste Collection Schedule | General waste, recycling and green-waste schedule sensors | Deployed | Sensors report the number of days until collection. |
| Bin Night household reminder | `notify.send_message` targeting the household notification group | Field tested | Runs at 19:00 when one or more bins are due the following day and dynamically lists the required bins. |

## Household chores and NFC

| System | Technology | Status | Notes |
|---|---|---|---|
| NFC task workflows | iPhone / Home Assistant NFC tags | Partial | Used for household/pet-care workflows. Public examples should use generic names and IDs rather than household-specific identifiers. |
| Companion App notifications | Home Assistant mobile app | Deployed | Individual device notification targets and a household notification group are in use. |

## System monitoring and diagnostics

| Area | Status | Notes |
|---|---|---|
| Router/WAN outage diagnostics | Active | ASUS GT-AX11000 syslogs are used for recurring outage investigation. Raw logs must be sanitized before publication. |
| Home Assistant integration faults | Active | Known examples include unavailable weather entities, Meross availability and changed/removed service actions. |
| Network topology documentation | In progress | Logical topology will live under `docs/network/`; private identifiers will not be included by default. |

## Known Home Assistant integrations to verify and document

The following integrations/components are known from the working installation or recent troubleshooting and should be audited against the live HA instance before the repository is considered complete:

- Amber Electric
- Automate Pulse / Pulse Pro
- BOM weather
- Ecowitt
- FarmBot
- Fronius
- HACS
- Meross
- MQTT
- Reolink
- Sigenergy
- Solcast
- Waste Collection Schedule
- legacy Aqua Temp / EVOHeat custom integration components

## Next inventory passes

1. Export a current Home Assistant device/entity inventory.
2. Map each important entity to its subsystem and dashboard.
3. Record integration installation method and upstream source.
4. Migrate working automation YAML in public-safe form.
5. Migrate dashboard YAML and document required custom cards.
6. Record tested HA/core/integration versions.
7. Add sanitized commissioning and troubleshooting examples.
