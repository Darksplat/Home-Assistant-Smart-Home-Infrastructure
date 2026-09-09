# Solar/energy Home Assistant integration and validation

This guide documents the Home Assistant-facing commissioning of the deployed solar and energy subsystem.

It is not an electrical-installation manual. Inverter, battery, meter and mains work must follow manufacturer instructions and applicable electrical requirements.

## 1. Required systems

The deployed Home Assistant design uses:

- Fronius GEN24 inverter integration;
- Sigenergy ESS integration;
- Amber Express integration;
- Solcast Solar integration;
- Home Assistant dashboards;
- a Fronius AC-power-limit automation.

The live integration inventory confirms all four core data/control integrations are present.

## 2. Bring monitoring online first

Before enabling any automated control, confirm each source independently.

### Sigenergy

Verify that Home Assistant receives sensible values for:

- battery state of charge;
- PV power;
- total site/load power;
- grid import power;
- grid export power;
- battery power.

The grid import/export values are the feedback source for the Fronius load-following automation.

### Fronius

Verify normal inverter telemetry is available.

Then confirm the Home Assistant integration exposes the AC power-limit controls used by the deployed automation:

```text
number.*_pv_ac_power_limit
switch.*_pv_ac_power_limiting
```

Entity names are installation-specific.

Do not enable automatic curtailment until manual test changes to the power limit have been observed and safely returned to 100%.

### Amber

Verify the current feed-in price entity updates and that negative values can be distinguished reliably from unavailable/unknown states.

### Solcast

Verify forecast data is updating. Solcast is useful to the dashboards/planning layer but is not required by the current negative-FIT Fronius control loop.

## 3. Manual Fronius control test

Before enabling the automation:

1. record current Fronius output and site flow;
2. enable the Fronius AC power-limiting switch;
3. reduce the limit to a conservative test value;
4. confirm inverter output responds;
5. restore the limit to 100%;
6. switch AC power limiting off;
7. confirm full normal operation resumes.

If the inverter does not respond exactly as expected, stop here and do not enable the automation.

## 4. Validate measurement direction

The automation assumes:

```text
grid export power > 0 when exporting
grid import power > 0 when importing
```

and calculates:

```text
net export = export - import
```

Confirm this sign convention using a period when the house is clearly importing and another when it is clearly exporting.

If the integration's sign convention changes, the control law must be revisited before use.

## 5. Deploy the automation

The current live automation is exported in:

```text
home-assistant/live-export/configuration/automations.yaml
```

Alias:

```text
Fronius - Amber Negative FIT Load Following
```

The control logic is documented in [CONTROL-LOGIC.md](CONTROL-LOGIC.md).

## 6. First controlled test

A safe first functional test requires:

- valid Amber feed-in price;
- battery SOC at/above the configured threshold;
- valid site import/export data;
- known-good Fronius power-limit controls;
- ability to disable the automation immediately if necessary.

Observe:

1. curtailment only activates under the intended negative-FIT/full-battery condition;
2. Fronius output changes in the expected direction;
3. grid export falls when the limit is reduced;
4. the limit does not oscillate aggressively;
5. the system returns to 100% / limiting off when the condition clears.

## 7. Dashboard validation

The live dashboard is:

```text
home-assistant/live-export/dashboards/energy-control-dashboard.yaml
```

Confirm the following frontend dependencies are installed:

- Mushroom Cards;
- card-mod;
- layout-card;
- Power Flow Card Plus.

Then verify:

- battery SOC is plausible;
- site PV, load and grid flows agree with the inverter/battery systems;
- import/export direction is visually correct;
- no custom-card errors are shown.

## 8. Commissioning checklist

- [ ] Sigenergy telemetry updating
- [ ] Fronius telemetry updating
- [ ] Amber feed-in price updating
- [ ] Solcast forecast updating
- [ ] Fronius limit controls manually tested
- [ ] grid import/export sign convention verified
- [ ] automation fail-safe path tested
- [ ] positive-FIT release tested
- [ ] battery-below-threshold release tested
- [ ] negative-FIT/full-battery curtailment tested
- [ ] Energy Max dashboard renders correctly
- [ ] limiting returns to 100% when automation is disabled/released

## 9. Change-management rule

Treat the working automation as operational infrastructure.

Before materially changing thresholds or control math:

1. copy the current known-good automation;
2. document the intended change;
3. change one tuning variable at a time;
4. observe at least one real import/export cycle;
5. retain the 100%-limit fail-safe path.
