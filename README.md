# Home Assistant Smart Home Infrastructure

Whole-home Home Assistant infrastructure, including dashboards, automations,
integrations, ESP32 devices, MQTT, Thread, networking, energy, weather,
hot water, garden systems, installation guides and troubleshooting
documentation.

## Purpose

This repository documents the Home Assistant installation and associated
smart-home infrastructure used in a real residential environment.

The goal is to maintain:

- reproducible Home Assistant configuration
- dashboards
- automations
- scripts
- templates
- entity mappings
- integration notes
- network and hardware architecture
- ESP32 and MQTT infrastructure
- Thread and Matter infrastructure
- installation procedures
- commissioning procedures
- troubleshooting records
- sanitized diagnostics
- links to specialised standalone projects

## Repository layout

### `home-assistant/`

Deployable or example Home Assistant configuration.

### `systems/`

Documentation and configuration grouped by functional system such as:

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

### `hardware/`

Hardware-specific documentation including Home Assistant hosts, ESP32
controllers, networking equipment and Thread infrastructure.

### `integrations/`

Installation, configuration and troubleshooting notes for Home Assistant
integrations.

### `inventory/`

System, device and entity inventories.

### `docs/`

Whole-system architecture, installation, security and troubleshooting
documentation.

### `diagnostics/`

Sanitized diagnostic material suitable for public sharing.

### `external-projects/`

References to related standalone repositories such as the EVOHeat and
FarmBot projects.

## Security

This is a public repository.

Passwords, API keys, authentication tokens, private certificates,
webhooks and other credentials must never be committed.

Use `secrets.yaml` locally and document required values in
`secrets.example.yaml`.

## Related projects

- EVOHeat EVO270 ESP32 / Modbus:
  https://github.com/Darksplat/EVOHeat-EVO270-ESP32-Modbus

- Home Assistant FarmBot:
  https://github.com/Darksplat/Homeassistant-Farmbot

## Status

This repository is being progressively populated from the working
Home Assistant installation.

Documentation and configuration should identify whether content is:

- field tested
- currently deployed
- experimental
- legacy
- example only
