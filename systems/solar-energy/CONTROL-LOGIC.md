# Fronius negative-FIT load-following control

This document explains the deployed Home Assistant automation:

```text
Fronius - Amber Negative FIT Load Following
```

The live configuration is exported in:

- [`home-assistant/live-export/configuration/automations.yaml`](../../home-assistant/live-export/configuration/automations.yaml)

## Objective

When Amber feed-in pricing becomes negative and the Sigenergy battery is full, excess Fronius PV can otherwise be exported to the grid at a cost.

The automation therefore reduces the Fronius AC output limit so the property consumes most of the remaining Fronius generation locally.

## Inputs

The deployed logic requires four live values:

- Amber feed-in price;
- Sigenergy battery state of charge;
- whole-site grid export power;
- whole-site grid import power.

If any of those values are unavailable, the automation disables curtailment and returns the Fronius limit to 100%.

## Triggering

The automation evaluates:

- every 30 seconds;
- whenever the Amber feed-in price changes;
- whenever battery state of charge changes.

It runs in `restart` mode so a new trigger supersedes an in-progress evaluation.

## State logic

### Case 1 — required data unavailable

Action:

```text
AC power limit → 100%
AC power limiting → OFF
```

This is the fail-safe path.

### Case 2 — feed-in tariff is zero or positive

Action:

```text
AC power limit → 100%
wait 2 s
AC power limiting → OFF
```

There is no reason for this automation to curtail the Fronius when export pricing is not negative.

### Case 3 — negative FIT, battery below 99%

Action:

```text
AC power limit → 100%
wait 2 s
AC power limiting → OFF
```

The battery is still available to absorb solar, so the automation does not curtail the Fronius.

### Case 4 — negative FIT, battery at or above 99%

If Fronius limiting is currently off:

```text
AC power limiting → ON
wait 3 s
```

The automation then uses site grid flow as feedback.

## Feedback calculation

The live automation calculates:

```text
net_export_kw = grid_export_kw - grid_import_kw
```

Interpretation:

- positive value = site is exporting;
- negative value = site is importing.

The automation only adjusts the Fronius limit when flow leaves the deadband:

```text
net_export_kw > 0.15
or
net_export_kw < -0.30
```

This asymmetric deadband intentionally tolerates a small amount of export and a somewhat larger amount of import before making another change.

## Power-limit calculation

For a 10 kW GEN24:

```text
1 kW = 10 percentage points
```

The automation uses:

```text
new_limit = current_limit - (net_export_kw × 10)
```

Then clamps the result:

```text
0% ≤ new_limit ≤ 100%
```

Examples:

| Current limit | Net grid flow | Calculated change | New limit |
| ---: | ---: | ---: | ---: |
| 60% | +0.50 kW export | -5 percentage points | 55% |
| 60% | -0.40 kW import | +4 percentage points | 64% |
| 20% | +3.00 kW export | -30 percentage points | 0% after clamp |
| 98% | -1.00 kW import | +10 percentage points | 100% after clamp |

## Why the controller is deliberately simple

The plant already contains native inverter and battery control systems. Home Assistant is only providing a supervisory layer to avoid paid export under a specific tariff condition.

The design therefore prioritises:

- predictable behaviour;
- easy inspection;
- a clear fail-safe state;
- bounded output;
- low control frequency;
- no dependence on perfect zero-flow tracking.

## Conditions that release curtailment

Curtailment is removed automatically when any of these become true:

- Amber FIT returns to zero/positive;
- battery SOC drops below 99%;
- any required sensor becomes unavailable.

The release sequence restores the limit to 100% and disables the Fronius limiting switch.

## Tuning notes

The following are tuning parameters, not universal constants:

```text
30 s evaluation interval
99% SOC threshold
+0.15 kW export threshold
-0.30 kW import threshold
10 percentage points per kW
```

Changes should be evaluated against real site behaviour, inverter response time and battery behaviour rather than adjusted solely for cosmetic dashboard smoothness.

## Safety rule

If future edits make the automation unstable, oscillatory or difficult to reason about, revert to the conservative state:

```text
AC power limit = 100%
AC power limiting = OFF
```

The native inverter/battery systems should always remain capable of operating independently of Home Assistant.
