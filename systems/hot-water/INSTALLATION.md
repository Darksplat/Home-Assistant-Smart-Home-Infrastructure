# EVO270 installation and commissioning

This document describes how the EVOHeat hot-water subsystem is commissioned into the whole-home Home Assistant installation.

For the exact firmware, wiring photos, Modbus register research and test sketches, use the dedicated repository:

- https://github.com/Darksplat/EVOHeat-EVO270-ESP32-Modbus

## 1. Hardware prerequisites

For each EVO270 unit:

- EVOHeat EVO270-1 with HW211-family controller;
- Waveshare ESP32-S3-RS485-CAN;
- suitable 5-pin JST-SM locking pigtail/harness;
- access to the Home Assistant Wi-Fi/LAN and MQTT broker;
- Arduino development environment for the current reference firmware.

The tested Waveshare board accepts the EVO270 accessory 12 V supply at its DC input. Never apply that voltage to a bare ESP32 5 V or 3.3 V pin.

## 2. Harness mapping

The field-tested EVO270 harness mapping is:

| EVO270 harness | Function | Waveshare terminal |
| --- | --- | --- |
| Red | +12 V DC | DC+ |
| Black | Ground | DC- |
| White | RS485 A | A+ |
| Yellow | RS485 B | B- |
| Orange | Shield / earth | Not connected on the tested installation |

Do not trust the wire order of an aftermarket pigtail. Verify connector position, continuity, polarity and function before applying power.

## 3. Modbus commissioning

Known-good serial settings:

```text
Modbus RTU
9600 baud
8 data bits
no parity
1 stop bit
slave 99 / 0x63
```

Waveshare UART/direction pins used by the reference implementation:

```text
TX  GPIO17
RX  GPIO18
EN  GPIO21
```

A useful commissioning test is register `2019` (T01 ambient temperature).

The proven decode for this register is:

```text
(raw - 60) * 0.5 °C
```

Do not move on to Home Assistant integration until a stable Modbus response can be read repeatedly from the controller.

## 4. Firmware

The working production approach uses direct Arduino code rather than ESPHome for the EVO270 RS485 controller.

The important RS485 direction sequence is:

1. set GPIO21 HIGH;
2. transmit the Modbus frame;
3. flush the UART;
4. wait for the short transmit guard delay;
5. set GPIO21 LOW;
6. receive and validate the reply.

On this exact installation, that explicit direction control resolved the partial-response/time-out behaviour seen during ESPHome testing.

Use the current read-only reference firmware from the dedicated EVOHeat repository. Copy its `secrets.example.h` to `secrets.h`, configure Wi-Fi/MQTT locally and never commit the real secrets file.

## 5. MQTT

The firmware publishes Home Assistant MQTT Discovery data and normal operating telemetry through the local MQTT broker.

Each controller derives a stable local namespace from its own Waveshare identity. Public documentation and dashboard templates use placeholders instead of real device IDs.

Validation before moving on:

- controller joins Wi-Fi;
- controller connects to MQTT;
- MQTT telemetry is updating;
- Home Assistant MQTT Discovery creates the expected device/entities;
- no duplicate or stale device identity is being confused with the old Aqua Temp module.

## 6. Home Assistant

Confirm the MQTT integration is active in Home Assistant.

After the controller connects and publishes discovery:

1. open **Settings → Devices & services → MQTT**;
2. confirm the EVO270 device is present;
3. check temperature/status/diagnostic entities;
4. leave the system running long enough to confirm values update at the expected polling intervals.

For this installation the normal polling pattern is approximately:

- fast data: every 20 seconds;
- slow/config data: every 5 minutes.

## 7. Dashboard

The deployed whole-home dashboard is exported at:

```text
home-assistant/live-export/dashboards/hot-water.yaml
```

The reusable fresh-install template is maintained in:

```text
Darksplat/EVOHeat-EVO270-ESP32-Modbus
home-assistant/dashboard/evo270-hot-water-dashboard.yaml
```

Frontend requirements:

- Mushroom Cards;
- card-mod.

For a fresh installation, import the public template and replace the generic unit placeholders with the actual Home Assistant entity IDs created by MQTT Discovery.

## 8. Validation checklist

Before declaring the subsystem commissioned, verify:

- [ ] EVO270 operates normally from its own controller;
- [ ] Waveshare powers reliably from the intended supply;
- [ ] Modbus register 2019 can be read repeatedly;
- [ ] no CRC/time-out errors are occurring continuously;
- [ ] Wi-Fi is stable;
- [ ] MQTT remains connected;
- [ ] Home Assistant device/entities are updating;
- [ ] temperatures are plausible;
- [ ] fault/status entities behave sensibly;
- [ ] both units appear independently;
- [ ] the Hot Water dashboard renders without missing-card errors;
- [ ] Mushroom Cards and card-mod are installed;
- [ ] legacy Aqua Temp entities are clearly distinguished from current MQTT entities.

## 9. Write-control policy

The current public firmware is read-only.

Do not enable arbitrary Modbus writes merely because a register appears writable. Any future control implementation should be:

- explicitly allow-listed;
- range checked;
- field tested on the actual EVO270 controller;
- designed so loss of Home Assistant/MQTT cannot compromise normal hot-water operation;
- documented with rollback/recovery behaviour.
