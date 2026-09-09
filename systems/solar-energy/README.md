# Solar and Energy

This subsystem documents the house-wide solar, battery, grid-price and export-control integration in Home Assistant.

## Status

**Deployed. Monitoring and local Fronius curtailment control are field tested.**

The live Home Assistant export confirms integrations for:

- Fronius;
- Sigenergy ESS;
- Amber Express;
- Solcast Solar;
- Electricity Maps / CO2 signal data;
- Home Assistant energy dashboards and control automation.

## System architecture

```text
Solar PV
  ├── Fronius GEN24 10 kW three-phase inverter
  └── Sigenergy / SigenStor energy-storage system

Grid / retailer data
  └── Amber Electric feed-in price

Forecast data
  └── Solcast PV forecast

All sources
  ↓
Home Assistant
  ├── Energy Max dashboard
  ├── Home Energy dashboard
  └── Fronius negative-FIT load-following automation
```

The Sigenergy integration provides the whole-site battery/load/import/export feedback used by the Fronius control automation.

## Main Home Assistant artefacts

### Dashboards

- [`home-assistant/live-export/dashboards/energy-control-dashboard.yaml`](../../home-assistant/live-export/dashboards/energy-control-dashboard.yaml)
- [`home-assistant/live-export/dashboards/home-energy.yaml`](../../home-assistant/live-export/dashboards/home-energy.yaml)

The main **Energy Max** dashboard includes live site flow, battery state of charge, PV generation, load, grid import/export and related energy information.

The deployed Energy Max dashboard uses custom frontend cards including:

- Mushroom Cards;
- card-mod;
- layout-card;
- Power Flow Card Plus.

### Automation

The deployed automation is contained in:

- [`home-assistant/live-export/configuration/automations.yaml`](../../home-assistant/live-export/configuration/automations.yaml)

Automation alias:

```text
Fronius - Amber Negative FIT Load Following
```

Its purpose is to locally curtail the Fronius GEN24 when Amber feed-in pricing is negative and the Sigenergy battery is effectively full, using whole-site grid flow as feedback.

## Control objective

During a negative feed-in tariff, exporting excess Fronius generation can incur a cost.

The automation therefore attempts to make the Fronius inverter follow the property's remaining load once the battery can no longer absorb excess energy.

Conceptually:

```text
Amber FIT >= 0
    → Fronius unrestricted

Amber FIT < 0 AND battery < 99%
    → Fronius unrestricted
    → battery remains available to absorb PV

Amber FIT < 0 AND battery >= 99%
    → enable Fronius AC power limiting
    → use site export/import feedback
    → adjust Fronius limit toward near-zero grid flow
```

## Fail-safe behaviour

The automation deliberately fails back to unrestricted Fronius operation if required input data becomes unavailable.

If Amber price, battery SOC, grid export or grid import data are not valid:

1. the Fronius AC power limit is set to 100%;
2. AC power limiting is switched off.

This prevents stale/missing Home Assistant data from leaving the inverter artificially curtailed.

## Load-following logic

The automation runs every 30 seconds and also reacts to Amber feed-in price and Sigenergy battery-SOC changes.

When curtailment is active:

```text
net export = grid export - grid import
```

The control deadband is currently:

```text
adjust if net export > +0.15 kW
or net export < -0.30 kW
```

For the 10 kW GEN24:

```text
1 kW ≈ 10 percentage points of inverter power limit
```

The next requested limit is calculated from the current limit and measured net grid flow, then clamped to 0–100%.

This is a simple feedback controller rather than a vendor-native energy-management system, so stability and fail-safe behaviour matter more than chasing exact zero flow every cycle.

## Key data sources

| Source | Home Assistant role |
| --- | --- |
| Sigenergy ESS | Battery SOC, PV, load, grid import/export and battery power |
| Fronius | Inverter monitoring and AC power-limiting controls |
| Amber Express | Dynamic import/feed-in pricing and negative-FIT signal |
| Solcast Solar | PV-generation forecast data |
| Electricity/CO2 data | Grid carbon/energy context where used |

## Privacy / portability

The sanitized live dashboards show the deployed design but may contain installation-specific entity names and location labels.

For reusable examples, prefer generic names such as:

```text
sensor.site_grid_export_power
sensor.site_grid_import_power
sensor.battery_state_of_charge
sensor.feed_in_price
number.fronius_ac_power_limit
switch.fronius_ac_power_limiting
```

## Documentation

- [Curtailment control logic](CONTROL-LOGIC.md)
- [Installation and validation](INSTALLATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Live automation export](../../home-assistant/live-export/configuration/automations.yaml)
- [Energy Max dashboard](../../home-assistant/live-export/dashboards/energy-control-dashboard.yaml)

## Operational caution

Home Assistant control is an additional supervisory layer. The Fronius and Sigenergy systems must remain safe and functional if Home Assistant, MQTT/LAN connectivity or external pricing services are unavailable.

Any future control changes should preserve the current fail-open behaviour unless there is a clearly documented reason not to.
