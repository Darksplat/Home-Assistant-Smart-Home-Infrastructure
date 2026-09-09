# Private recovery requirements

This public repository deliberately omits material that would make the household less secure. A genuinely recoverable Home Assistant installation therefore needs a **separate private recovery set**.

This document lists what should exist privately; it does not contain the values themselves.

## Critical private items

Keep at least two current copies, with one copy stored separately from the Home Assistant host.

- [ ] Recent Home Assistant full backup
- [ ] Home Assistant backup encryption/recovery information where applicable
- [ ] `secrets.yaml` or a secure record of every value needed to recreate it
- [ ] Router/LAN administration recovery information
- [ ] Private DHCP/static-address reservations required by fixed infrastructure
- [ ] MQTT credentials if authentication is enabled
- [ ] Wi-Fi credentials needed by ESP/IoT devices
- [ ] Thread operational dataset / migration material if preserving the existing Thread network
- [ ] Matter setup/commissioning codes retained according to device/vendor guidance
- [ ] ESPHome YAML and secrets for devices whose raw configuration is intentionally excluded from the public export
- [ ] Private add-on/app configuration that contains credentials
- [ ] Private household chores/NFC package and dashboard material
- [ ] Cloud integration account access / MFA recovery information
- [ ] Private certificates/keys if the installation uses them

## Why these are separate

The public GitHub repository is intended to answer:

- what systems exist;
- how they are connected;
- what Home Assistant configuration/automations are deployed;
- how to commission and troubleshoot them.

It should **not** answer:

- how to authenticate as a household member;
- how to join the private Thread/Wi-Fi/MQTT networks;
- which private mobile device belongs to which person;
- what tokens or API keys are valid;
- what private addressing or credentials unlock infrastructure.

## Recovery-set maintenance

Whenever one of the following changes, update the private recovery set as well as the public documentation where appropriate:

- router replacement/reset;
- Home Assistant host migration;
- Thread border-router migration;
- Matter fabric/device recommissioning;
- ESPHome device replacement;
- MQTT credential changes;
- major custom-integration reauthentication;
- household notification-device replacement;
- addition of an important locally controlled device.

## Test, don't assume

A backup that has never been restored is not a proven recovery path. Periodically verify that:

1. the backup can be opened/recognized;
2. the recovery credentials are available away from the HA host;
3. the private ESPHome/Thread/network records are readable;
4. the public repository plus private recovery set together explain how to rebuild critical systems.

Do not commit the private recovery set, screenshots of credentials, raw QR codes, Thread datasets or password exports to this repository.
