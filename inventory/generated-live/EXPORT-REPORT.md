# Home Assistant export report

Generated: `2026-09-09T13:39:15+10:00`
Source mount: `/Volumes/config`

## Generated counts

- **areas:** 26
- **custom components:** 12
- **dashboards:** 12
- **devices:** 163
- **entities:** 2688
- **esphome yaml files:** 3
- **integration domains:** 41
- **integration entries:** 54

## Copied/sanitized text configuration

- `configuration.yaml`
- `automations.yaml`
- `scripts.yaml`
- `scenes.yaml`
- `packages/duino_coin.yaml`
- `packages/household_chores.yaml`
- `themes/minimalist-desktop/minimalist-desktop.yaml`
- `themes/minimalist-ios-tapbar/minimalist-ios-tapbar.yaml`
- `themes/minimalist-mobile/minimalist-mobile.yaml`
- `themes/minimalist-mobile-tapbar/minimalist-mobile-tapbar.yaml`

## Redactions applied

- None detected

## Skipped items

- None

## Always excluded by design

- `secrets.yaml`
- `.storage/auth*`, `http.auth`, `mobile_app`, `person`
- `.storage/thread.datasets`
- `.storage/core.config_entries` raw contents (used only to count integration domains)
- databases and WAL/SHM files
- logs and fault logs
- backups and ZIP/TAR archives
- SSL/private keys/certificates
- raw ESPHome YAML
- raw custom-component source code
- add-on/app credential stores

## Review requirement

This exporter is deliberately conservative, but generated files should still be reviewed before merging into a public repository.
