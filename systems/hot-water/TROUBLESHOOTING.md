# EVO270 troubleshooting

This guide covers the Home Assistant-facing EVO270 subsystem. For low-level protocol captures and test firmware, see the dedicated EVOHeat repository.

## Quick fault isolation

Work from the heat pump outward:

```text
EVO270 controller
  ↓
RS485 wiring
  ↓
Waveshare ESP32
  ↓
Wi-Fi
  ↓
MQTT broker
  ↓
Home Assistant MQTT entities
  ↓
Dashboard
```

Do not start by changing the dashboard if the underlying MQTT entities are stale or unavailable.

## No Modbus response

Check:

1. EVO270 is powered and operating normally;
2. Waveshare has the correct DC supply;
3. RS485 A/B polarity is correct;
4. controller address is `99` / `0x63`;
5. serial format is 9600 8N1;
6. TX/RX/EN pins match the reference implementation;
7. GPIO21 direction control switches back to receive after transmit;
8. register 2019 can be read with the known-good commissioning sketch.

If register 2019 cannot be read reliably, solve that before testing the full firmware.

## Partial `FE` responses / time-outs

This behaviour was encountered during ESPHome commissioning on the tested Waveshare + EVO270 installation.

The working Arduino implementation explicitly controls RS485 direction:

```text
EN HIGH → transmit → UART flush → guard delay → EN LOW → receive
```

If you see one-byte/partial responses or repeated time-outs, compare the code path with the known-good Arduino commissioning sketch in the dedicated EVOHeat repository.

## MQTT device does not appear in Home Assistant

Check in this order:

1. controller Wi-Fi connection;
2. MQTT broker address and credentials in the local secrets file;
3. controller MQTT connection state/log output;
4. Mosquitto broker status in Home Assistant;
5. MQTT integration status;
6. whether discovery messages are being published;
7. whether a stale retained discovery payload is causing a duplicate/old device.

Never commit MQTT credentials while troubleshooting.

## Entities appear but do not update

Check:

- controller MQTT connection remains active;
- fast poll data changes at roughly 20-second intervals;
- slow/config entities are allowed up to roughly 5 minutes;
- the ESP32 has not rebooted repeatedly;
- Modbus reads are still succeeding;
- Home Assistant has not lost connection to the MQTT broker.

A dashboard card showing `unavailable` is normally a symptom, not the root cause.

## Temperatures look wrong

Start with the known-good ambient-temperature register and decode.

For register 2019:

```text
°C = (raw - 60) * 0.5
```

If that value is implausible:

- confirm the correct register is being read;
- confirm byte ordering;
- confirm CRC validation;
- compare raw data with the commissioning capture;
- verify the controller model/protocol family really matches the documented HW211 installation.

## Duplicate EVO270 devices/entities

The installation has historical Aqua Temp integration data as well as the current local MQTT path.

Avoid mixing the two namespaces.

For new/local commissioning:

- treat MQTT Discovery devices as the current implementation;
- treat Aqua Temp entities as legacy unless deliberately being used for comparison;
- do not rename a new Waveshare controller to impersonate the removed cloud/Wi-Fi module;
- use fresh Home Assistant device/entity identities.

## Dashboard shows missing custom cards

The deployed/public dashboard requires:

- Mushroom Cards;
- card-mod.

If cards display configuration errors, confirm those frontend resources are installed and loaded before editing entity IDs or dashboard logic.

## Dashboard shows `Entity not found`

The public reusable dashboard uses generic placeholders.

For a fresh installation:

1. wait for MQTT Discovery to create both EVO270 devices;
2. find the actual entities under Home Assistant's device/entity pages or Developer Tools;
3. replace the unit placeholders in the dashboard template;
4. verify both units independently.

The sanitized whole-home live export also aliases installation-specific hardware IDs, so it should be treated as documentation of layout/logic, not a literal drop-in configuration for another home.

## Old Controller Clocks cards are missing

That is expected in the local MQTT-only design.

The historical clock-sync cards depended on the Aqua Temp custom integration and its service/entity model. They are not a dependency of the current read-only Arduino + MQTT implementation.

## One unit works, the other does not

Treat each EVO270/Waveshare pair independently.

Check:

- power to the second Waveshare;
- its local RS485 harness;
- its Wi-Fi connection;
- its MQTT client/device identity;
- its Home Assistant discovery entities;
- accidental duplicate client IDs or topics.

A working first unit proves the overall Home Assistant/MQTT design but does not prove the second RS485 harness or controller path.

## Fault entity is active

Do not clear or override an EVO270 fault through speculative Modbus writes.

First:

1. verify the fault/state is current rather than stale MQTT data;
2. inspect the EVO270's own controller/display;
3. identify the controller fault normally;
4. use the heat-pump manufacturer's service procedure where appropriate.

Home Assistant is a monitoring layer and should not bypass native safety behaviour.

## Recovery rule

If troubleshooting changes begin to make the system less predictable, return to the simplest known-good path:

1. EVO270 native operation unchanged;
2. known-good single-register Arduino commissioning sketch;
3. verify register 2019;
4. restore the read-only reference firmware;
5. verify MQTT;
6. verify Home Assistant entities;
7. only then restore dashboard/customisation work.
