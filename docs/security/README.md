# Security and Public Repository Policy

This repository documents a real residential Home Assistant installation, so public reproducibility must be balanced against household privacy and credential security.

## Never publish

Do not commit:

- Home Assistant access tokens
- passwords
- API keys
- MQTT credentials
- Wi-Fi credentials
- webhook identifiers/secrets
- private certificates or keys
- authentication cookies
- cloud integration tokens
- Thread operational datasets
- raw `.storage` authentication/config-entry data
- MAC addresses or unnecessary stable hardware identifiers
- complete device/entity registry inventories
- personal Companion App device labels
- household-member-specific chore data
- unreviewed diagnostic logs or backups

## Live export policy

The repository uses `tools/ha-export/run-export.sh` to read selected material from the mounted Home Assistant `/config` share.

The export is intentionally not a backup. It applies two layers:

1. **selection/redaction during export** — only approved configuration, dashboard and aggregate inventory material is copied;
2. **post-export public-safety pass** — generated files are further anonymised and scanned before review.

The safety pass currently:

- removes MAC/hardware addresses
- removes email addresses
- aliases opaque hardware/vendor identifiers
- aliases `notify.mobile_app_*` service targets
- removes the live household chores package/dashboard
- removes complete device/entity registry inventories
- scans for Bearer tokens
- scans for secret-bearing URLs
- scans deployable configuration for credential-like assignments
- flags possible globally routable IPv4 addresses

A successful run ends with:

```text
PUBLIC SAFETY PASS: clean
```

This is a guardrail, not permission to commit blindly. The diff still receives human review.

## Files that remain private

Important Home Assistant source files that are never copied wholesale include:

- `secrets.yaml`
- `.storage/auth*`
- `.storage/http.auth`
- `.storage/person`
- `.storage/mobile_app`
- `.storage/thread.datasets`
- raw `.storage/core.config_entries`
- Home Assistant databases
- logs/fault logs
- backups and archives
- SSL/private keys
- raw ESPHome YAML
- third-party custom-component source

## Secrets handling

Use `!secret` references in Home Assistant configuration where appropriate and keep the real `secrets.yaml` outside Git.

`secrets.example.yaml` may document required key names using placeholders only.

## Privacy handling

Some information is not a credential but is still inappropriate for the public repository. Examples include personal device names, family-member workflow assignments and exhaustive room-to-device registry mappings.

The public repository therefore publishes curated subsystem documentation and aggregate counts rather than raw registry dumps.

## Diagnostics and troubleshooting

Before committing logs, screenshots, packet captures or diagnostics:

1. remove credentials/tokens
2. remove MAC addresses and public IPs
3. remove account/email identifiers
4. remove serial numbers where unnecessary
5. remove household-specific personal details
6. retain only the material needed to explain the technical fault

Raw captures belong outside the public repository.
