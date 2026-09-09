# Installation and rebuild

This section is the recovery/rebuild entry point for the Home Assistant installation documented by this repository.

The repository is designed to preserve **architecture, public-safe configuration, dashboards, automations and subsystem knowledge**. It is not a substitute for a Home Assistant full backup: credentials, authentication stores, Thread operational datasets, Companion App identities, private household data and some device-specific configuration are deliberately excluded from this public repository.

## Recovery strategy

Use the following order of preference.

### Level 1 — restore a Home Assistant full backup

A recent, tested Home Assistant backup is the fastest and most complete recovery path. It can preserve data that this public repository intentionally cannot contain.

After restoring the backup:

1. confirm Home Assistant starts cleanly;
2. confirm the network and DNS path are working;
3. check MQTT, Matter Server and Thread/OTBR;
4. verify critical integrations;
5. test critical automations manually;
6. run the repository export workflow and compare the restored system with the documented baseline.

### Level 2 — repository-assisted rebuild

Use this when the original Home Assistant instance or usable backup is unavailable.

A repository-assisted rebuild can recreate the documented architecture and public configuration, but some integrations will require fresh authentication, discovery, pairing or private recovery data.

## Rebuild order

The order matters. Restore infrastructure first, then integrations, then UI/automation layers.

### Phase 1 — platform and network

1. Install a supported Home Assistant OS release on the replacement host.
2. Complete initial onboarding locally.
3. Set the correct timezone, locale and network configuration.
4. Confirm the host can reach the LAN, DNS and internet before adding integrations.
5. Re-establish any private DHCP reservations or infrastructure addressing from the private network record.

Do not copy old `.storage` files into a new installation by hand.

### Phase 2 — private recovery material

Before rebuilding integrations, restore the private items listed in [`PRIVATE-RECOVERY-REQUIREMENTS.md`](PRIVATE-RECOVERY-REQUIREMENTS.md).

At minimum this normally includes:

- `secrets.yaml` or equivalent credentials;
- current Home Assistant backups;
- private network/DHCP information;
- Thread recovery material if the Thread network must be preserved;
- ESPHome source/secrets for locally managed ESP devices;
- any private household-specific package/dashboard material;
- credentials or account access needed to re-authenticate cloud integrations.

None of those secrets should be copied into this public repository.

### Phase 3 — Home Assistant apps/services

Install and start the infrastructure services required by the current installation:

- Mosquitto broker / MQTT service;
- Matter Server;
- OpenThread Border Router where used by the current Thread topology;
- ESPHome Device Builder for ESP device maintenance;
- Samba share for the repository export workflow;
- Terminal & SSH for local administration when required.

Validate each service before moving on. For example, do not troubleshoot an MQTT device before confirming the MQTT broker itself is healthy.

### Phase 4 — integrations

Rebuild integrations in dependency order rather than alphabetically.

Recommended sequence:

1. MQTT;
2. Thread / OTBR / Matter;
3. local network integrations such as Fronius, Sigenergy, Reolink, Ecowitt, Rain Bird, Meross LAN and Automate Pulse Pro;
4. HACS and required custom integrations;
5. weather/forecast integrations;
6. cloud/tariff/forecast services such as Amber and Solcast;
7. media, appliance and secondary integrations;
8. Companion App devices last, because their entity/service names may change during a rebuild.

See [`DEPENDENCIES.md`](DEPENDENCIES.md) and [`../../integrations/README.md`](../../integrations/README.md).

### Phase 5 — frontend dependencies

Install the HACS/frontend components required by the dashboards before importing the dashboards. Otherwise dashboards can appear broken even when their entities are healthy.

See [`FRONTEND-DEPENDENCIES.md`](FRONTEND-DEPENDENCIES.md).

### Phase 6 — configuration

Use the public live export as a **reference and restoration source**, not as an instruction to overwrite a new `/config` tree blindly.

The current public configuration snapshot is under:

```text
home-assistant/live-export/configuration/
```

Review and restore, as applicable:

- `configuration.yaml` sections;
- automations;
- scripts;
- scenes;
- approved public packages;
- themes.

Entity IDs created by a clean rebuild may differ from the old installation. Resolve those differences before enabling automations.

### Phase 7 — dashboards

Dashboard exports are under:

```text
home-assistant/live-export/dashboards/
```

Restore dashboards after their integrations and frontend dependencies exist. Import one dashboard at a time and resolve unavailable entities before proceeding to the next.

The live Household dashboard is intentionally excluded from the public repository and must be restored from private material if required.

### Phase 8 — subsystem commissioning

Commission high-impact systems individually:

1. network and Home Assistant infrastructure;
2. energy monitoring, then solar curtailment control;
3. hot-water monitoring;
4. weather;
5. security cameras/doorbell;
6. blinds and Thread/Matter devices;
7. garden/FarmBot/irrigation;
8. garage;
9. letterbox;
10. waste collection/notifications;
11. remaining secondary integrations.

Each subsystem README under [`../../systems/`](../../systems/) contains its operating logic and troubleshooting boundary.

### Phase 9 — automations

Do not enable all automations immediately after a clean rebuild.

For each automation:

1. confirm every referenced entity/service exists;
2. run its template expressions manually where practical;
3. test actions with harmless/manual triggers;
4. confirm any physical actuator moves in the intended direction;
5. then enable normal scheduling/triggers.

This is particularly important for:

- Fronius curtailment;
- irrigation/pump sequencing;
- blind movement;
- garage control;
- notification routing.

### Phase 10 — final validation

Use [`RECOVERY-CHECKLIST.md`](RECOVERY-CHECKLIST.md) as the final acceptance checklist.

After the rebuilt system is stable, mount the Home Assistant Samba `config` share and run:

```bash
zsh tools/ha-export/run-export.sh
```

The export must finish with:

```text
PUBLIC SAFETY PASS: clean
```

Review the Git diff. The new export should explain intentional changes rather than silently replacing the known-good baseline.

## What the public repository cannot restore by itself

A public clone alone is intentionally insufficient to recreate every private identity or credential. Expect to restore or re-create the following outside GitHub:

- account credentials and tokens;
- Home Assistant users/authentication state;
- Companion App registrations;
- Thread operational credentials and some Matter commissioning state;
- private ESPHome secrets/source not exported here;
- household-specific chores/NFC assignments;
- exact entity registry IDs where Home Assistant regenerates them;
- private network reservations/addresses that are not required for public reproducibility.

That boundary is intentional: the repository should be useful enough to rebuild the system without becoming a public copy of the household's security material.
