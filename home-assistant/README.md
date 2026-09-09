# Home Assistant Configuration

This directory contains public-safe Home Assistant configuration and the repeatable sanitized live export.

## Rebuild entry point

For a host restore or clean rebuild, start with:

- [`../docs/installation/README.md`](../docs/installation/README.md) — ordered rebuild procedure
- [`../docs/installation/DEPENDENCIES.md`](../docs/installation/DEPENDENCIES.md) — service/integration dependency matrix
- [`../docs/installation/FRONTEND-DEPENDENCIES.md`](../docs/installation/FRONTEND-DEPENDENCIES.md) — dashboard/HACS requirements
- [`../docs/installation/RECOVERY-CHECKLIST.md`](../docs/installation/RECOVERY-CHECKLIST.md) — final acceptance checklist

A Home Assistant full backup remains the preferred exact recovery method. This public repository intentionally excludes credentials, authentication state, Thread datasets and other private recovery material.

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

The `live-export/` tree is evidence of what is deployed; curated directories are where installation-neutral examples and subsystem packages can be developed.

## Safety boundary

Never commit the working `/config/.storage` directory or credentials.

The export workflow runs `tools/ha-export/public_safety.py`, which removes or aliases private identifiers and deletes material unsuitable for the public repository. A clean run ends with `PUBLIC SAFETY PASS: clean`.

It then runs `tools/repo-audit/dashboard_dependencies.py` to generate a current custom-frontend dependency inventory from the dashboards that remain public.

The Git diff still requires review before merge.
