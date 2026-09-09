# Smart Home Subsystems

This directory contains curated documentation for each functional subsystem in the deployed Home Assistant installation.

Subsystem documentation is intentionally separated from the generated live export. Generated evidence under `home-assistant/live-export/` is a sanitized snapshot of the running system; files under `systems/` explain how the installation is assembled, what depends on what, how to validate it, and how to troubleshoot it.

## Documented subsystems

- `hot-water/` — EVOHeat EVO270 local Modbus/MQTT monitoring
- `solar-energy/` — Fronius, Sigenergy, Amber and Solcast energy system
- `weather/` — Ecowitt local station plus Bureau of Meteorology forecasts
- `garden-farmbot/` — FarmBot, Rain Bird irrigation and pump/power control
- `blinds/` — Automate/Pulse roller-blind control and blind dashboard
- `thread-matter/` — Home Assistant Thread/Matter stack and commissioned devices
- `security/` — Reolink NVR, PoE cameras, doorbell and chimes
- `garage/` — Meross LAN garage-door integration
- `letterbox-sentinel/` — DIY MQTT mail/parcel monitoring
- `waste-collection/` — bin schedule sensors and household reminder automation
- `network/` — Home Assistant-facing network services and recovery boundaries
- `system-monitoring/` — host, app, integration and infrastructure health monitoring
- `notifications/` — public-safe notification architecture
- `duino-coin/` — REST-based miner monitoring and dashboard
- `household-chores/` — public-safe design notes for the private household chores/NFC workflow

## Public repository rule

Subsystem documentation should explain architecture and reproducible behaviour without publishing credentials, Thread datasets, raw mobile-device identities, stable hardware identifiers, private household assignments, or unnecessary internal addressing.
