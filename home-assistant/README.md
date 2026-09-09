# Home Assistant Configuration

This directory contains public-safe Home Assistant configuration.

Configuration should be grouped into reusable components wherever practical.

## Structure

- `packages/` - grouped HA packages
- `automations/` - automation YAML
- `scripts/` - scripts
- `templates/` - template entities and supporting YAML
- `dashboards/` - Lovelace dashboard YAML
- `themes/` - themes
- `blueprints/` - blueprints
- `helpers/` - helper definitions/documentation
- `mqtt/` - MQTT-related configuration and documentation

Do not commit the working `/config/.storage` directory or any credentials.
