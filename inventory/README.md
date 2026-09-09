# Infrastructure Inventory

This directory contains the public-safe inventory for the working Home Assistant installation.

The repository deliberately separates **generated live evidence** from **curated system documentation**:

- `generated-live/` is produced from the mounted Home Assistant `/config` share by `tools/ha-export/`;
- `system-inventory.md` is the human-readable subsystem inventory derived from that live evidence.

## Current live baseline

The 9 September 2026 source snapshot reported:

- 26 Home Assistant areas
- 163 registry devices before privacy filtering
- 2,688 registry entities before privacy filtering
- 54 integration entries across 41 integration domains
- 12 storage-mode Lovelace dashboards before privacy filtering
- 12 custom components
- 3 ESPHome YAML files present on the live host

The full device and entity registry tables are **not published**. They contain much more household-specific detail than is required for a public infrastructure repository. Aggregate counts remain in `generated-live/EXPORT-REPORT.md`.

## Generated public-safe inventory

`generated-live/` contains or, after the next export refresh, generates:

- `areas.md` — Home Assistant area names
- `integrations.md` — integration domains and config-entry counts
- `custom-components.md` — custom integration manifest metadata and versions
- `esphome-files.md` — ESPHome YAML filenames only, never the credential-bearing YAML
- `EXPORT-REPORT.md` — source snapshot counts and exported-file summary
- `PUBLIC-SAFETY-SCAN.md` — privacy/credential guardrail results
- `FRONTEND-DEPENDENCIES.md` — custom Lovelace card/layout dependencies derived from the retained public dashboards

Detailed device and entity registry inventories are generated only transiently during export and are removed by the public-safety pass.

## Curated inventory

[`system-inventory.md`](system-inventory.md) maps the live Home Assistant evidence into functional systems such as energy, weather, hot water, garden, cameras, blinds, Matter/Thread, MQTT and waste collection.

The curated inventory should record:

- system role
- Home Assistant integration path
- dashboard/configuration evidence
- public repository location
- related standalone repository where applicable
- documentation status

## Recovery use

The generated inventory is useful during a rebuild to answer:

- which integration domains existed;
- which custom components were installed and their captured versions;
- which dashboard frontend dependencies are required;
- how many major areas/integration entries were present at the baseline.

It is not a substitute for a full Home Assistant backup or the private recovery set described in `docs/installation/PRIVATE-RECOVERY-REQUIREMENTS.md`.

## Public repository policy

Do not publish:

- credentials, tokens, API keys or authentication material
- MAC addresses or stable hardware identifiers
- raw Home Assistant device/entity registries
- personal Companion App device names
- Thread datasets
- household-member-specific chore data
- raw ESPHome configuration
- unreviewed diagnostics or logs

The public inventory is intended to make the architecture reproducible without turning the repository into a map of private household identity data.
