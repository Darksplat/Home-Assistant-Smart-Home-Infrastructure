# Solar and energy troubleshooting

Use this guide when the Energy Max dashboard, Amber-driven curtailment or Fronius control does not behave as expected.

## Work from measurements before control

Use this order:

```text
Sigenergy / Fronius / Amber source data
        ↓
Home Assistant entities
        ↓
control conditions
        ↓
Fronius limiting entities
        ↓
automation
        ↓
dashboard
```

Do not tune the control loop while its input data are stale or wrong.

## Automation never curtails

Check all required conditions:

- Amber feed-in price is actually below zero;
- battery state of charge is at least 99%;
- grid import/export entities are available;
- Fronius AC power limiting entity exists and can be switched on;
- the number entity controlling AC power limit is writable;
- the automation is enabled.

The deployed logic deliberately does **not** curtail while the battery SOC is below 99%.

## Automation immediately releases curtailment

This can be correct behaviour.

The automation returns the Fronius to 100% / limiting off when:

- any required sensor is unavailable;
- Amber FIT is zero or positive;
- battery SOC falls below 99%.

Check entity history around the release event rather than assuming the automation failed.

## Fronius limit changes but export does not fall

Check:

1. whether the Fronius inverter is actually producing enough power for the limit to matter;
2. whether the limit entity represents percent of rated power as expected;
3. whether another inverter/battery component is supplying the export;
4. whether whole-site grid data are updating quickly enough;
5. whether the Fronius control switch remains enabled;
6. whether the integration/device ignored or reverted the requested limit.

The site contains more than one energy source, so not every export change is attributable to the Fronius alone.

## Controller oscillates between import and export

Some movement around zero is expected. The controller intentionally uses a deadband.

Current adjustment thresholds:

```text
export > +0.15 kW
import > 0.30 kW (net export < -0.30 kW)
```

If oscillation becomes excessive:

- verify measurement latency first;
- confirm the 30-second control interval has not been shortened;
- confirm the Fronius takes effect before the next evaluation;
- avoid increasing gain until timing/measurement problems are ruled out;
- return the system to 100% / limiting off if behaviour becomes unpredictable.

## Home Assistant sensor values disagree with vendor apps

Check timestamps and measurement scope.

Possible causes include:

- inverter-only versus whole-site measurement;
- different refresh intervals;
- battery power being included/excluded differently;
- stale Home Assistant data;
- integration rounding;
- import/export sign conventions.

For the curtailment automation, the important feedback is the Sigenergy whole-site grid import/export pair used by the live configuration.

## Amber price is unavailable

When Amber data is unavailable the automation should fail open:

```text
Fronius limit → 100%
limiting → OFF
```

Do not substitute a guessed or stale price value for control purposes.

Check the Amber Express integration status and whether the current feed-in price entity is updating.

## Sigenergy data is unavailable

If SOC or site grid-flow data are unavailable, automatic Fronius curtailment is intentionally disabled.

Check:

- Sigenergy integration availability;
- network connectivity to the local system where applicable;
- integration diagnostics/logs;
- whether the expected entity names changed after an integration update.

Do not bypass the availability check just to make the automation run.

## Fronius control entities are missing

Check the Fronius integration/device entities and whether advanced/control entities are disabled.

The deployed automation expects two control concepts:

```text
AC power limiting enabled/disabled
AC power limit percentage
```

If the integration changes entity names or behaviour, update the automation only after manually confirming the replacement entities.

## Fronius limit is stuck below 100%

First disable the automation, then manually restore:

```text
AC power limit = 100%
AC power limiting = OFF
```

Confirm the inverter resumes normal output.

Then inspect why the automation's release/fail-safe path did not execute. Pay particular attention to entity renames, failed service calls or changes in integration semantics.

## Dashboard power-flow direction looks wrong

The dashboard and automation may use different but related power entities.

Verify the underlying numeric entity states first. Do not fix a visual arrow by changing the automation's sign convention unless the actual measured import/export direction is wrong.

## Missing custom cards

Energy Max uses custom frontend components including:

- Mushroom Cards;
- card-mod;
- layout-card;
- Power Flow Card Plus.

If the dashboard shows card configuration errors, repair those HACS/frontend resources without changing the underlying energy automation.

## Solcast unavailable

Solcast forecast loss should affect forecast/display features, not the current negative-FIT Fronius feedback loop.

Keep forecast troubleshooting separate from live curtailment troubleshooting unless future automation explicitly introduces forecast dependence.

## Recovery procedure

For uncertain or unstable behaviour:

1. disable the Fronius negative-FIT automation;
2. set the Fronius AC limit to 100%;
3. switch AC power limiting off;
4. verify normal native inverter/battery operation;
5. verify Amber, Sigenergy and Fronius sensors independently;
6. manually test Fronius limiting;
7. re-enable the automation only after all measurements/control entities are known good.

The native energy system should never depend on Home Assistant being available in order to operate safely.
