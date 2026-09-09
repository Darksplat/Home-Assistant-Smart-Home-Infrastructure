# Hot Water dashboard

Live Home Assistant dashboard for the two EVOHeat EVO270 hot-water systems in this installation.

## Status

- Source: live Home Assistant storage-mode Lovelace dashboard (`.storage/lovelace.hot_water`)
- Exported: September 2026
- Layout: Home Assistant Sections view
- Views: 1
- Sections: 5
- Cards: 70
- Field status: currently deployed on the working Home Assistant installation

This directory deliberately keeps both the exact exported dashboard configuration and a YAML-compatible copy so the original live structure is preserved before any later templating or cleanup work.

## Files

### `hot-water-dashboard.json`

Exact public-safe export of the live Lovelace `data.config` object. The Home Assistant `.storage` wrapper is not included.

### `hot-water-dashboard.yaml`

YAML-compatible copy of the same live dashboard configuration. It intentionally preserves JSON-style mapping/list syntax rather than rewriting the dashboard during the first extraction pass. JSON object syntax is valid YAML-compatible structured data and preserving the exact structure avoids introducing semantic changes while establishing the repository baseline.

A later repository pass may add a separately normalised/template-oriented YAML version with installation-specific entity IDs replaced by placeholders.

## Dashboard scope

The dashboard presents both installed EVO270 systems side by side:

- Bathroom & Laundry
- Ensuite & Kitchen

For each system it exposes the current Home Assistant entities for:

- current water temperature
- target water temperature
- operating mode
- ambient temperature
- tank bottom temperature
- tank top temperature
- coil temperature
- suction temperature
- solar/auxiliary temperature
- controller-display temperature
- compressor state
- electrical booster state
- defrost state
- disinfection/high-temperature stage
- MQTT/API status
- Modbus-link status
- fault status
- unit power
- disinfection target, duration, start-hour and cycle readback

The dashboard also contains prominent visual states for heating, faults, connection failures and disinfection operation.

## Dependencies

### Required Home Assistant frontend components

The live dashboard uses:

- **Mushroom Cards** (`custom:mushroom-template-card`)
- **card-mod** for dynamic CSS/card styling
- standard Home Assistant Sections, Grid, Heading, Conditional and Tile cards

Mushroom Cards and card-mod are normally installed through HACS on this installation.

## EVO270 integration dependency

The dashboard depends on the local EVOHeat ESP32 / MQTT entity set used by this Home Assistant system.

Full hardware, RS485, Modbus, ESP32, MQTT and commissioning documentation is maintained separately at:

https://github.com/Darksplat/EVOHeat-EVO270-ESP32-Modbus

The specialised EVOHeat repository remains the authoritative source for the heat-pump hardware/interface project. This repository documents how those entities are consumed by the whole-home Home Assistant installation.

## Installation-specific entity IDs

The exact live export contains entity IDs generated for the two installed controllers. These IDs are installation-specific and should not be assumed to exist on another Home Assistant system.

Before using this dashboard elsewhere, map the two controller namespaces to the entities created by that installation. A future public template will replace the live unit identifiers with explicit placeholders.

## Importing into Home Assistant

For an existing storage-mode dashboard:

1. Install Mushroom Cards and card-mod and confirm both frontend resources load correctly.
2. Confirm the required EVO270 entities already exist in Home Assistant.
3. Create or open the target dashboard.
4. Open the dashboard menu and select **Raw configuration editor**.
5. Replace the configuration with the contents of the exported dashboard file.
6. Replace installation-specific entity IDs with the matching entities for the target system.
7. Save and verify every card before relying on controls.

Do not blindly import this dashboard into a system that does not have the matching EVO270 entity set.

## Controls and current limitations

The live dashboard contains Home Assistant controls for the entities exposed as writable by the current installation, including target temperature and operating mode.

The timer/disinfection schedule area is intentionally read-only. The current dashboard explicitly reports that writable timer entities are not yet exposed by the MQTT firmware, so it does not present controls that could falsely imply a schedule change succeeded.

The controller clock is also not currently exposed by the local MQTT firmware. The dashboard therefore shows Home Assistant time as the reliable reference rather than inventing a controller-time value.

## Public-repository safety

This export contains no passwords, API keys, tokens, credentials or webhook values. The original Home Assistant `.storage` file is not committed.

The source `.storage` directory remains private and must never be copied wholesale into this public repository.
