# Frontend and dashboard dependencies

The live dashboards are storage-mode Lovelace exports. Their YAML/JSON can be preserved in Git, but several dashboards also depend on HACS/frontend resources that must be installed separately.

## Known minimum frontend set

The current public dashboards demonstrate use of the following custom frontend components:

| Frontend component | Observed use |
| --- | --- |
| Mushroom Cards | Hot Water, Energy, Garden, Reolink and other status cards |
| card-mod | Styling across multiple dashboards |
| layout-card / `custom:grid-layout` | Energy, Garden and Home Operations responsive layouts |
| button-card | Roller Blinds, Home Operations/Waste Collection and Duino-Coin |
| weather-forecast-card | Weather Operations Centre and Home Operations |
| power-flow-card-plus | Energy Max live power-flow display |
| ApexCharts Card | Letterbox Sentinel battery visualization |

This is a **minimum known set**, not a promise that no additional custom card appears in a later dashboard revision.

## Rebuild procedure

1. Install HACS and restart Home Assistant if required by the HACS installation process.
2. Install the current compatible release of each required frontend component.
3. Confirm its Lovelace resource is registered and loads without a browser-console error.
4. Clear/reload the browser frontend if a newly installed card still reports `Custom element doesn't exist`.
5. Import dashboards only after their custom cards are available.
6. Resolve unavailable entities separately from frontend-card errors; they are different failure classes.

## Typical failure messages

### `Custom element doesn't exist: mushroom-template-card`

Install/repair Mushroom Cards and confirm the resource loaded.

### `Custom element doesn't exist: layout-card`

Install/repair layout-card. Dashboards using `custom:grid-layout` will not render correctly without it.

### `Custom element doesn't exist: button-card`

Install/repair button-card. This affects advanced cards in the blinds, waste/home operations and Duino-Coin dashboards.

### `Custom element doesn't exist: power-flow-card-plus`

Install/repair Power Flow Card Plus. Energy telemetry may still be healthy even though the graphical flow card is missing.

### `Custom element doesn't exist: apexcharts-card`

Install/repair ApexCharts Card. Letterbox entities can still be tested from Developer Tools while the chart component is unavailable.

## Dashboard dependency audit

Before treating this file as current after a major dashboard change, inspect the generated dashboard files under:

```text
home-assistant/live-export/dashboards/
```

Search for `custom:` card types and `card_mod:` blocks. The repository also contains a small audit helper under `tools/repo-audit/` to list custom card types from the JSON dashboard exports.

## Browser/device considerations

A dashboard that works on one browser but fails on another can indicate stale frontend resources rather than a Home Assistant backend problem. During recovery, test at least one desktop browser and one normal Home Assistant client before changing entity configuration to fix a rendering-only issue.
