# Recovery acceptance checklist

Use this checklist after a Home Assistant restore, host migration or repository-assisted rebuild.

Do not mark the recovery complete because the dashboard loads. Validate each dependency layer and each actuator that can affect the physical house.

## Platform

- [ ] Home Assistant starts without restart loops
- [ ] Correct timezone and locale are configured
- [ ] LAN, DNS and internet connectivity are working
- [ ] Home Assistant backup schedule is re-established
- [ ] Samba/export access is available if required
- [ ] Terminal/SSH administrative path works if intentionally enabled

## Core services

- [ ] MQTT integration is connected to the broker
- [ ] Mosquitto broker is healthy
- [ ] Matter Server is healthy
- [ ] Thread integration is healthy
- [ ] OTBR/border-router path is healthy where applicable
- [ ] ESPHome maintenance environment is available
- [ ] HACS loads normally

## Frontend

- [ ] Mushroom Cards load
- [ ] card-mod styling loads
- [ ] layout-card / custom grid layouts load
- [ ] button-card loads
- [ ] weather forecast custom card loads
- [ ] Power Flow Card Plus loads
- [ ] ApexCharts Card loads
- [ ] No persistent `Custom element doesn't exist` errors remain on public dashboards

## Energy and solar

- [ ] Fronius telemetry is current
- [ ] Sigenergy telemetry is current
- [ ] Grid import/export direction is sensible
- [ ] Battery SOC is sensible
- [ ] Amber feed-in price is available
- [ ] Solcast forecast is available
- [ ] Fronius curtailment switch/limit entities exist
- [ ] Negative-FIT automation has been manually reviewed before enabling
- [ ] Fail-open/full-output behaviour has been verified

## Hot water

- [ ] Both EVO270 systems appear in MQTT/Home Assistant
- [ ] Temperature values are plausible
- [ ] Compressor/booster/defrost/disinfection states are plausible
- [ ] Fault state is available
- [ ] No Modbus writes have been enabled unless separately validated
- [ ] Hot Water dashboard loads without missing frontend dependencies

## Weather

- [ ] Ecowitt gateway data is current
- [ ] Outdoor temperature/humidity are plausible
- [ ] Wind/rain/UV/solar-radiation sensors update
- [ ] BOM weather entities update
- [ ] Daily and hourly forecasts load
- [ ] Weather Operations Centre loads on desktop and mobile-sized client

## Garden / FarmBot / irrigation

- [ ] FarmBot integration responds
- [ ] FarmBot power outlet state is correct
- [ ] Pressure pump outlet state is correct
- [ ] Rain Bird zones respond individually
- [ ] Weather data used by garden dashboard is current
- [ ] Graceful shutdown sequence resolves correctly
- [ ] Watering automation is tested manually before scheduled use
- [ ] Pump is never left running unintentionally after a failed test

## Blinds / Thread / Matter

- [ ] All intended blind cover entities are available
- [ ] Each blind opens/closes in the correct direction
- [ ] Position feedback is plausible
- [ ] Dog Door partial-position behaviour is verified
- [ ] Blind battery sensors are available where expected
- [ ] Morning automation timing is correct for current DST state
- [ ] Sunset automation is tested
- [ ] Matter devices survive a Home Assistant restart

## Security / access

- [ ] Reolink NVR/integration is connected
- [ ] Doorbell stream loads
- [ ] Representative front/rear camera streams load
- [ ] Detection entities update
- [ ] Chime controls respond
- [ ] Garage door state is accurate before testing movement
- [ ] Garage open/close control is tested while physically observing the door

## Letterbox

- [ ] Mail Sentinel telemetry is available when awake
- [ ] Mail-waiting state behaves correctly
- [ ] Parcel sensor is online
- [ ] Battery states are plausible
- [ ] Clear/reset controls work
- [ ] Test notification is received through intended public-safe notification route

## Waste collection and notifications

- [ ] General waste sensor returns a day count
- [ ] Recycling sensor returns a day count
- [ ] Green waste sensor returns a day count
- [ ] `notify.household_notifications` exists
- [ ] A manual test notification reaches the intended household devices
- [ ] Bin reminder template correctly identifies bins due tomorrow

## Secondary systems

- [ ] Duino-Coin REST data updates if retained
- [ ] Roborock integration is healthy
- [ ] Synology monitoring is healthy
- [ ] TV/MusicCast/Cast integrations are healthy where required
- [ ] Browser Mod functions used by dashboards work

## Repository verification

- [ ] Mount the live Home Assistant `config` Samba share
- [ ] Run `zsh tools/ha-export/run-export.sh`
- [ ] Export finishes with `PUBLIC SAFETY PASS: clean`
- [ ] Review `inventory/generated-live/EXPORT-REPORT.md`
- [ ] Review `inventory/generated-live/PUBLIC-SAFETY-SCAN.md`
- [ ] Review the Git diff before commit
- [ ] Update subsystem documentation if architecture materially changed

## Recovery complete

Only call the recovery complete when critical physical systems have been observed working and the repository/private recovery records match the rebuilt installation.
