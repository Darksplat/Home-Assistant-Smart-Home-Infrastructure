# Bulk Home Assistant exporter

This tool turns the mounted live Home Assistant `/config` share into a conservative, public-safe repository export in one pass.

## What it exports

The exporter reads the live Home Assistant files from the Mac Samba mount and generates:

- selected top-level YAML configuration (`configuration.yaml`, `automations.yaml`, `scripts.yaml`, `scenes.yaml` when present)
- `packages/` and `themes/` text configuration
- storage-mode Lovelace dashboards from `.storage/lovelace.*`
- dashboard JSON plus YAML-compatible copies
- Home Assistant area inventory
- device inventory without identifiers, MAC addresses, serial numbers or unique IDs
- entity inventory without registry unique IDs
- integration-domain/count inventory
- custom-component manifest inventory without copying third-party source code
- ESPHome YAML filename inventory without copying ESPHome credentials/configuration
- an export report listing redactions and skipped items
- an automatic post-export public-safety report

Generated output is written under:

```text
home-assistant/live-export/
inventory/generated-live/
```

## What it deliberately does NOT export

The tool does not publish the following into the repository:

- `secrets.yaml`
- `.storage` wholesale
- authentication data
- `http.auth`
- raw mobile-app data
- person data
- Thread datasets
- raw `core.config_entries`
- databases, WAL or SHM files
- Home Assistant logs
- backups/archives
- SSL/private keys/certificates
- raw ESPHome YAML
- raw custom-component source code
- add-on/app credential stores
- the live household chores package/dashboard
- Home Assistant Companion App device/entity inventory rows

`core.config_entries` is read only to produce aggregate integration-domain counts. Its raw contents are never written to the repository.

## Automatic public-safety pass

`run-export.sh` performs two stages:

1. export/sanitize the selected Home Assistant material;
2. post-process and validate the generated repository files.

The safety pass automatically:

- removes MAC/hardware addresses and email addresses;
- aliases long hardware/vendor-generated hexadecimal identifiers so stable device IDs are not published;
- aliases `notify.mobile_app_*` targets to generic household-device names;
- removes Companion App devices/entities from the public inventories;
- removes the live household chores package and household dashboard, which contain household-member-specific assignments;
- checks for Bearer tokens, secret-bearing URLs and credential-like assignments;
- checks exported Home Assistant data for possible globally routable IPv4 addresses.

The resulting report is written to:

```text
inventory/generated-live/PUBLIC-SAFETY-SCAN.md
```

If high-risk findings remain, the script exits with an error and prints `EXPORT NOT READY FOR PUBLIC COMMIT`.

The safety pass only operates on generated files inside the repository. It does not modify the live Home Assistant Samba share.

## Running it on this installation

The Home Assistant Samba `config` share is mounted on the Mac at:

```text
/Volumes/config
```

From the repository root run:

```bash
zsh tools/ha-export/run-export.sh
```

Or explicitly run the exporter and safety pass:

```bash
python3 tools/ha-export/export_home_assistant.py \
  --source /Volumes/config \
  --repo /Users/jeremyyounger/Documents/GitHub/Home-Assistant-Smart-Home-Infrastructure

python3 tools/ha-export/public_safety.py \
  --repo /Users/jeremyyounger/Documents/GitHub/Home-Assistant-Smart-Home-Infrastructure
```

The exporter only reads the Home Assistant share. It never modifies files on the Pi.

## After running

Review both:

```text
inventory/generated-live/EXPORT-REPORT.md
inventory/generated-live/PUBLIC-SAFETY-SCAN.md
```

Then run:

```bash
git status --short
```

Do not blindly commit material if either report contains unexpected warnings or redactions. The repository is public, so generated files still receive a review before merge.

## Repeat exports

The generated directories are rebuilt each time the script runs. This makes later Home Assistant snapshots repeatable: mount Samba, run one command, review the diff, commit/push, and GitHub shows exactly what changed in the live system.

## Dashboard format

Storage-mode dashboards are exported from the `data.config` object only; the Home Assistant `.storage` wrapper is discarded.

Each retained dashboard is written as both `.json` and `.yaml`. The `.yaml` copy deliberately uses JSON object syntax, which is YAML 1.2-compatible. This preserves the structure without requiring PyYAML or introducing formatting/semantic changes during extraction.

The public snapshot is intentionally sanitized rather than a byte-for-byte deployment copy. Hardware-derived entity fragments and personal mobile notification targets may therefore appear as aliases such as `deviceid_001` or `notify.mobile_app_household_device_01`.
