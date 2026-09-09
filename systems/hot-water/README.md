# Hot Water — EVOHeat EVO270

This subsystem documents the two **EVOHeat EVO270-1** heat-pump hot-water systems integrated with Home Assistant through local ESP32/RS485 monitoring.

## Status

**Deployed and field tested for local read-only monitoring.**

The working production path is:

```text
EVOHeat EVO270-1 / HW211 controller
        │
        │ RS485 / Modbus RTU — 9600 8N1
        ▼
Waveshare ESP32-S3-RS485-CAN
        │
        │ Wi-Fi / MQTT
        ▼
Mosquitto broker
        │
        ▼
Home Assistant MQTT integration
        │
        ├── entities / diagnostics
        └── Hot Water dashboard
```

The detailed firmware, protocol research, wiring, Modbus map and commissioning history remain in the dedicated project:

- [EVOHeat-EVO270-ESP32-Modbus](https://github.com/Darksplat/EVOHeat-EVO270-ESP32-Modbus)

This whole-home repository documents how that project fits into the wider Home Assistant installation.

## Installed equipment

| Component | Role |
| --- | --- |
| 2 × EVOHeat EVO270-1 | Heat-pump hot-water systems |
| HW211-family controller | Native EVO270 controller / Modbus endpoint |
| 2 × Waveshare ESP32-S3-RS485-CAN | Local RS485-to-MQTT controllers |
| Mosquitto broker | MQTT transport into Home Assistant |
| Home Assistant MQTT integration | Device/entity discovery and state ingestion |
| Mushroom Cards + card-mod | Frontend dependencies for the deployed dashboard |

## Proven communications settings

| Setting | Value |
| --- | --- |
| Protocol | Modbus RTU |
| Baud | 9600 |
| Serial format | 8N1 |
| Controller/slave address | 99 (`0x63`) |
| ESP32 UART TX | GPIO17 |
| ESP32 UART RX | GPIO18 |
| RS485 direction / enable | GPIO21 |
| Known-good test register | 2019 / T01 ambient temperature |
| Fast polling | 20 seconds |
| Slow/config polling | 5 minutes |

These values are field-proven on this installation. The standalone EVOHeat repository contains the commissioning captures and register research.

## Home Assistant implementation

The current production firmware publishes through MQTT and uses MQTT Discovery to create Home Assistant devices and entities.

The live whole-home export contains the deployed dashboard at:

- [`home-assistant/live-export/dashboards/hot-water.yaml`](../../home-assistant/live-export/dashboards/hot-water.yaml)
- [`home-assistant/live-export/dashboards/hot-water.json`](../../home-assistant/live-export/dashboards/hot-water.json)

The exported dashboard currently contains:

- 1 view;
- 5 Sections-layout sections;
- 70 cards;
- status, temperatures and diagnostic information for both hot-water systems.

The public fresh-install dashboard template lives in the dedicated EVOHeat repository and uses generic unit placeholders rather than installation-specific device identities.

## What is deliberately separated

The repository keeps two different artefacts for two different purposes:

### Whole-home live export

The dashboard and configuration under `home-assistant/live-export/` show how the subsystem is deployed in this Home Assistant installation after privacy sanitisation.

### Reusable EVO270 project

The standalone EVOHeat repository contains:

- firmware;
- hardware/wiring documentation;
- Modbus register information;
- MQTT design;
- commissioning sketches;
- reproducible Home Assistant dashboard template;
- ESPHome interoperability findings;
- protocol diagnostics.

This avoids duplicating firmware/protocol work in the whole-home repository while still documenting the subsystem relationship.

## Local-control objective

The local ESP32/RS485 path removes normal monitoring dependence on the original Aqua Temp cloud/Wi-Fi module.

The current public reference firmware is intentionally **read-only**. Monitoring is proven; arbitrary Modbus writes are not part of the public production implementation.

That restriction is important because EVO270 controller parameters can affect compressor protection, anti-freeze logic, disinfection and other safety-related behaviour.

## Legacy Aqua Temp integration

The Home Assistant installation still contains historical/legacy Aqua Temp entities for comparison and migration purposes. They should not be confused with the current local MQTT path.

Where both entity families are visible:

- **MQTT entities** represent the current local ESP32 path;
- **Aqua Temp entities** are legacy cloud/custom-integration data.

New installations should use the local MQTT design documented in the standalone project rather than trying to preserve the old Aqua Temp device identity.

## Frontend dependencies

The deployed/public dashboards use:

- Mushroom Cards;
- card-mod;
- Home Assistant built-in Sections/Grid/Heading/Tile/Conditional cards.

Install the maintained frontend dependencies through HACS rather than copying third-party source code into this repository.

## Documentation

- [Installation and commissioning](INSTALLATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Dedicated EVO270 firmware/protocol project](https://github.com/Darksplat/EVOHeat-EVO270-ESP32-Modbus)
- [Live Hot Water dashboard](../../home-assistant/live-export/dashboards/hot-water.yaml)

## Safety

Disconnect/isolate mains power before opening the EVO270 enclosure. The low-voltage accessory/RS485 connector is located inside equipment that also contains mains-voltage wiring.

Verify connector function and polarity before applying power. Do not assume an aftermarket JST-SM pigtail has the same wire order as the original EVO270 harness.
