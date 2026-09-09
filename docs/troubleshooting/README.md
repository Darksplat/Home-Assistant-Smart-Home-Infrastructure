# Troubleshooting and recovery

This is the whole-system troubleshooting entry point. Subsystem-specific faults should then be followed into the relevant `systems/<subsystem>/` documentation.

Only sanitized logs and diagnostic information should be committed to the public repository.

## Diagnose by layer

Do not start by editing dashboard YAML. Work from the lowest failed dependency upward.

```text
Power / physical device
        ↓
LAN / Wi-Fi / Thread / RS485 connectivity
        ↓
Broker / server / Home Assistant app
        ↓
Home Assistant integration
        ↓
Entities
        ↓
Automations / templates
        ↓
Dashboard / frontend
```

A red dashboard card can be caused by any layer below it.

## First five questions

1. Is the physical device powered and otherwise functional?
2. Is the underlying network/radio/protocol path healthy?
3. Is the required Home Assistant app/service running?
4. Does the integration show an error or unavailable entities?
5. Did the fault begin after a reboot, update, network change or device replacement?

## Whole-home outage triage

When many unrelated integrations fail together, suspect shared infrastructure first.

Check in this order:

1. router/LAN and upstream internet where relevant;
2. Home Assistant host health;
3. DNS;
4. switch/Wi-Fi/backhaul health;
5. MQTT broker;
6. Matter Server / OTBR for Thread/Matter failures;
7. integration-specific devices.

Do not factory-reset individual IoT devices while a shared network fault is still plausible.

## Home Assistant host problems

### UI unavailable

Check whether the host itself responds on the LAN before troubleshooting integrations. If the host is unreachable, restore host/network access first.

### UI loads but many integrations are unavailable

Check Home Assistant logs, app health and LAN/DNS. A single integration failure should not normally take unrelated local integrations offline.

### Database/log fault after unclean shutdown

Preserve diagnostics before destructive action. Prefer recovery from a known-good Home Assistant backup over manually manipulating the database unless there is a specific reason and a backup exists.

## MQTT faults

Symptoms can include missing EVO270 data, DIY sensor unavailability or devices appearing offline.

Check:

1. Mosquitto broker app is running;
2. Home Assistant MQTT integration is connected;
3. DNS/LAN path between publishers and broker;
4. device MQTT connection state;
5. discovery/state topics only after transport is proven.

Do not modify Modbus/device firmware merely because MQTT delivery failed.

## Thread / Matter faults

Separate these failure classes:

- Matter Server unavailable;
- OTBR/border-router unavailable;
- Thread network problem;
- one commissioned Matter device offline;
- Home Assistant entity problem.

Avoid deleting the Thread network or recommissioning every Matter device as a first response. See `systems/thread-matter/`.

## Dashboard/frontend faults

A dashboard can fail while backend entities remain healthy.

Check for:

- `Custom element doesn't exist` — missing HACS/frontend resource;
- cards showing `unavailable` — likely entity/integration issue;
- styling/layout only broken — card-mod/layout-card/browser cache;
- one browser broken while another works — stale frontend cache/resource state.

See `docs/installation/FRONTEND-DEPENDENCIES.md`.

## Automation faults

When an automation fails:

1. inspect its trace;
2. identify the first failed condition/action;
3. verify referenced entity IDs still exist;
4. verify service/action syntax against the running Home Assistant version;
5. test templates in Developer Tools;
6. test physical actions manually before re-enabling schedules.

Never assume an automation is safe merely because it was valid YAML.

## Safe recovery rules for physical actuators

For solar curtailment, pumps, irrigation, blinds and garage control:

- observe the physical system during testing;
- prefer fail-safe/default states;
- test one actuator at a time;
- stop immediately if state feedback disagrees with reality;
- do not enable unattended schedules until manual validation passes.

## Subsystem routing

| Symptom | Start here |
| --- | --- |
| Hot-water values/faults | `systems/hot-water/TROUBLESHOOTING.md` |
| Solar/battery/curtailment | `systems/solar-energy/TROUBLESHOOTING.md` |
| Weather/BOM/Ecowitt | `systems/weather/README.md` |
| FarmBot/irrigation/pump | `systems/garden-farmbot/README.md` |
| Blind control/batteries | `systems/blinds/README.md` |
| Matter/Thread | `systems/thread-matter/README.md` |
| Reolink streams/detections | `systems/security/README.md` |
| Garage door | `systems/garage/README.md` |
| Letterbox/parcel | `systems/letterbox-sentinel/README.md` |
| Bin reminders | `systems/waste-collection/README.md` |
| Notifications | `systems/notifications/README.md` |
| Network-wide failures | `systems/network/README.md` and `docs/network/README.md` |
| HA host/apps | `systems/system-monitoring/README.md` |
| Duino-Coin | `systems/duino-coin/README.md` |

## Capturing a useful troubleshooting case

A public troubleshooting record should contain:

- date/time window;
- symptom;
- affected systems;
- what was still working;
- relevant sanitized logs/events;
- tests performed;
- root cause if established;
- proven recovery;
- prevention/follow-up.

Remove tokens, credentials, public addresses, MACs, private household identities and unreviewed raw logs before commit.

## After a major recovery

Use `docs/installation/RECOVERY-CHECKLIST.md`, then regenerate the sanitized live snapshot with:

```bash
zsh tools/ha-export/run-export.sh
```

A recovery is not complete until the physical systems are validated and the repository accurately reflects the rebuilt architecture.
