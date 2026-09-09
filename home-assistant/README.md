# Home Assistant Configuration

This directory contains public-safe Home Assistant configuration and the repeatable sanitized live export.

## Generated live baseline

`live-export/` is rebuilt from the mounted Home Assistant `/config` Samba share by:

```bash
zsh tools/ha-export/run-export.sh
```

The export currently includes selected top-level configuration, public-safe packages/themes and storage-mode dashboards. It does **not** include secrets, raw `.storage`, raw ESPHome YAML, full registry inventories or household-specific private material.

### `live-export/configuration/`

Sanitized copies of currently deployed text configuration such as:

- `configuration.yaml`
- `automations.yaml`
- `scripts.yaml`
- `scenes.yaml`
- approved packages
- themes

### `live-export/dashboards/`

Public dashboard exports extracted from `.storage/lovelace.*` using only the Lovelace `data.config` object.

Each retained dashboard is exported as both JSON and YAML-compatible structured data.

## Curated configuration structure

The non-generated directories remain the place for reusable/documented configuration as subsystem work is curated:

- `packages/` — grouped HA packages
- `automations/` — reusable/documented automation YAML
- `scripts/` — scripts
- `templates/` — template entities and supporting YAML
- `dashboards/` — curated/template Lovelace dashboard configuration
- `themes/` — themes
- `blueprints/` — blueprints
- `helpers/` — helper definitions/documentation
- `mqtt/` — MQTT-related configuration and documentation

The `live-export/` tree is the evidence of what is deployed; curated directories are where installation-neutral examples and subsystem packages can be developed.

## Safety boundary

Never commit the working `/config/.storage` directory or credentials.

The export workflow runs `tools/ha-export/public_safety.py`, which removes or aliases private identifiers and deletes material that is unsuitable for the public repository. A clean run ends with `PUBLIC SAFETY PASS: clean`, but the Git diff still requires review before merge.
