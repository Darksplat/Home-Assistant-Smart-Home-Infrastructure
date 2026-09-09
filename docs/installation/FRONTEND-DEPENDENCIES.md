# Frontend and dashboard dependencies

The live dashboards are storage-mode Lovelace exports. Their YAML/JSON can be preserved in Git, but several dashboards also depend on HACS/frontend resources that must be installed separately.

## Current generated inventory

The exporter now audits every public JSON dashboard after privacy filtering and writes the authoritative current component-use report to:

```text
inventory/generated-live/FRONTEND-DEPENDENCIES.md
```

The 9 September 2026 baseline scans 11 public dashboards and detects 12 custom element/configuration names. Those 12 names collapse to **nine installable frontend packages** because `grid-layout` is supplied by layout-card, while the three `mushroom-*` card types are supplied by Mushroom Cards.

## Required installable frontend packages

| Installable package | Dashboard component names observed | Observed dashboard use |
| --- | --- | --- |
| ApexCharts Card | `apexcharts-card` | Garden, Energy Max, Letterbox Sentinel, Weather Operations Centre |
| Button Card | `button-card` | Duino-Coin, Home Operations, Roller Blinds |
| card-mod | `card_mod` configuration blocks | Garden, Reolink, Energy Max, Home Operations, Hot Water, Weather Operations Centre |
| Helios Card | `helios-card` | Home Energy |
| layout-card | `layout-card`, `grid-layout` | Garden, Energy Max, Home Operations |
| Mushroom Cards | `mushroom-entity-card`, `mushroom-template-card`, `mushroom-title-card` | Duino-Coin, Home Operations, Garden, Reolink, Energy Max, Hot Water, Letterbox Sentinel |
| Power Flow Card Plus | `power-flow-card-plus` | Energy Max, Home Operations |
| Weather Forecast Card | `weather-forecast-card` | Home Operations, Weather Operations Centre |
| Windrose Card | `windrose-card` | Weather Operations Centre |

Install the maintained Home Assistant-compatible release of each package through HACS or the component's supported installation method.

The generated report, not this prose table, is the source of truth for which custom element names are present after a future dashboard refresh.

## Rebuild procedure

1. Install HACS and restart Home Assistant if required by the HACS installation process.
2. Install all nine currently required frontend packages listed above.
3. Confirm each Lovelace resource is registered and loads without a browser-console error.
4. Re-run the live export/dependency audit if restoring from a newer repository snapshot and compare the generated inventory with the installed set.
5. Clear/reload the browser frontend if a newly installed card still reports `Custom element doesn't exist`.
6. Import or restore dashboards only after their custom cards are available.
7. Resolve unavailable entities separately from frontend-card errors; they are different failure classes.

## Typical failure messages

### `Custom element doesn't exist: mushroom-template-card`

Install/repair Mushroom Cards and confirm the resource loaded. The same package provides the observed Mushroom entity, template and title cards.

### `Custom element doesn't exist: layout-card` or `grid-layout`

Install/repair layout-card. The deployed responsive layouts use both `custom:layout-card` and `custom:grid-layout`.

### `Custom element doesn't exist: button-card`

Install/repair Button Card. This affects advanced cards in Roller Blinds, Home Operations and Duino-Coin.

### `Custom element doesn't exist: power-flow-card-plus`

Install/repair Power Flow Card Plus. Energy telemetry can remain healthy even though the graphical flow card is missing.

### `Custom element doesn't exist: apexcharts-card`

Install/repair ApexCharts Card. Underlying entities can still be tested from Developer Tools while charts are unavailable.

### `Custom element doesn't exist: helios-card`

Install/repair Helios Card. The current Home Energy dashboard is the public dashboard that depends on it.

### `Custom element doesn't exist: windrose-card`

Install/repair Windrose Card. The current Weather Operations Centre uses it for wind visualization.

### `Custom element doesn't exist: weather-forecast-card`

Install/repair Weather Forecast Card. This is used by Home Operations and the Weather Operations Centre.

## Dashboard dependency audit

The normal export command:

```bash
zsh tools/ha-export/run-export.sh
```

now performs the frontend dependency audit automatically after the public-safety pass.

For a standalone audit against the already exported public dashboards, run:

```bash
python3 tools/repo-audit/dashboard_dependencies.py
```

The audit reads:

```text
home-assistant/live-export/dashboards/*.json
```

and writes:

```text
inventory/generated-live/FRONTEND-DEPENDENCIES.md
```

This should be reviewed whenever dashboard configuration changes materially.

## Browser/device considerations

A dashboard that works on one browser but fails on another can indicate stale frontend resources rather than a Home Assistant backend problem. During recovery, test at least one desktop browser and one normal Home Assistant client before changing entity configuration to fix a rendering-only issue.
