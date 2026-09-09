# Home Assistant integrations

This directory documents the integration layer used by the working Home Assistant installation.

The sanitized live baseline recorded **54 config entries across 41 integration domains**. Raw `core.config_entries` data is intentionally not published because it can contain credentials and installation-specific identifiers.

## Evidence sources

- `inventory/generated-live/integrations.md` — configured integration domains and counts
- `inventory/generated-live/custom-components.md` — custom-component manifest names/versions/upstream links
- `systems/` — subsystem-specific operating and troubleshooting documentation
- `docs/installation/DEPENDENCIES.md` — rebuild order and dependency matrix

## Integration classes

### Core/local integrations

Important local or built-in integrations represented by the baseline include:

- MQTT
- Matter
- Thread
- OTBR
- Fronius
- Ecowitt
- Rain Bird
- Reolink
- Roborock
- Synology DSM
- LG webOS TV
- Yamaha MusicCast
- Google Cast
- UPnP
- Bluetooth
- Met.no

Most of these should be rebuilt from Home Assistant's normal UI/discovery workflow rather than by copying `.storage` files from another installation.

### Custom integrations

The custom-component inventory currently records:

| Domain | Component | Snapshot version | Upstream / role |
| --- | --- | --- | --- |
| `amber_express` | Amber Express | 2.0.1 | Dynamic tariff data |
| `aqua_temp` | Aqua Temp | 3.0.37 | Hot-water integration evidence; local EVO270 MQTT project does not require it for read-only monitoring |
| `automate_pulse_pro` | Automate Pulse Pro | 1.0.0 | Roller blinds |
| `browser_mod` | Browser Mod | 3.2.3 | Browser/frontend services |
| `bureau_of_meteorology` | Bureau of Meteorology | 1.3.5 | Australian weather data |
| `farmbot` | FarmBot | 0.4.1 | FarmBot integration |
| `hacs` | HACS | 2.0.5 | Custom package manager |
| `meross_cloud` | Meross Cloud IoT | 1.3.12 | Installed component; no active `meross_cloud` config entry in the generated baseline |
| `meross_lan` | Meross LAN | 5.8.0 | Local Meross devices / garage / garden switching |
| `sigen` | Sigenergy ESS | 1.2.7.3 | Sigenergy local energy telemetry |
| `solcast_solar` | Solcast PV Forecast | v4.6.1 | PV forecast |
| `waste_collection_schedule` | Waste Collection Schedule | 2.32.0 | Bin schedule sensors |

Version numbers are the captured baseline, not a blanket recommendation to downgrade or upgrade. During a rebuild, first check compatibility with the Home Assistant version being installed.

## HACS rebuild principle

Do not restore the entire HACS/custom-component directory from an unreviewed old copy simply because the dashboard needs custom cards.

Preferred flow:

1. install HACS using its current supported installation method;
2. restart Home Assistant as required;
3. install required custom integrations from their maintained upstream repositories;
4. restart/reload according to each integration's instructions;
5. add/configure integrations through Home Assistant;
6. install frontend dependencies listed in `docs/installation/FRONTEND-DEPENDENCIES.md`;
7. only then restore dashboards.

This reduces the chance of carrying incompatible cached code into a new Home Assistant release.

## Re-authentication

The repository cannot restore cloud/account authentication by design. Expect to re-authenticate integrations such as tariff/forecast/cloud services and household mobile devices from the Home Assistant UI.

Never put exported auth tokens, cookies, MFA recovery material or raw config-entry JSON into this repository.

## Entity identity after rebuild

A clean integration setup can produce entity IDs different from the old installation. Before enabling automations:

1. compare expected entities in the relevant subsystem README/dashboard;
2. map any new entity IDs;
3. update curated configuration if necessary;
4. test templates and actions manually;
5. then enable schedules/physical actions.

Avoid renaming entities solely to make a dashboard look clean until the underlying integration is confirmed healthy.

## Troubleshooting hierarchy

When an integration fails, diagnose in this order:

1. physical device/service power;
2. LAN/radio connectivity;
3. required broker/server/app;
4. Home Assistant integration state;
5. entity availability;
6. automation/template logic;
7. dashboard rendering.

This prevents a frontend symptom from being mistaken for an integration failure.
