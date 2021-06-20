[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<br><a href="https://www.buymeacoffee.com/azogue" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-black.png" width="150px" height="35px" alt="Buy Me A Coffee" style="height: 35px !important;width: 150px !important;" ></a>

> **_WARNING:_ This library is deprecated**, as it is not needed anymore :) See details [here](https://github.com/azogue/fasthue/issues/22)

# Fast-Hue customizer

Custom integration to **modify the fixed update interval (5s)** of the main `hue` integration.

It is configured only by UI, and creates a sensor entity for each Hue bridge, showing the current polling interval.
It also register a new service **`fasthue.set_update_interval`** to be able to change the update interval dynamically, even from automations or scripts.

## Installation

Place the `custom_components` folder in your configuration directory
(or add its contents to an existing `custom_components` folder).

## Configuration

Add it using the Configuration->Integrations menu of Home Assistant, set the desired new update interval, and you're good to go.

If there are more than 1 hue bridge, all of them will get the same update interval. Created sensors live under the Hue bridge device, as they are linked to each hub.

When the integration is removed, the sensor entities are deleted, the service dissapears,
and the update interval is set again to 5 seconds, like nothing happened,
so you can try it with no danger :)

### Dynamic update interval

With the integration already installed, the update interval can be changed dynamically by 2 methods: using a service call for each bridge, or changing it globally.

#### Set update interval with a service call for each Hue bridge

Once configured, the new `fasthue.set_update_interval` service is available to use with each bridge (:= sensor entity),
so different refresh intervals can be set for different bridges, and they can be changed anytime.

The YAML data to call this service is:

```yaml
service: fasthue.set_update_interval
data:
  scan_interval: 7
target:
  entity_id: sensor.hue_polling_interval
```

Take into account that the scan interval modification done with this service call won't persist a HA restart. At that moment, the original value will be back.

#### Change update interval globally

It is now possible to change the interval for all bridges by clicking in the "Options" button of the Fast-Hue integration.
This is equivalent to removing the integration and adding it again with another value, but looks nicer :)

### Automation example

A slider (:= `input_number`) to dynamically change the refresh rate on a hue bridge:

```yaml
input_number:
  hue_polling_interval:
    name: "Hue polling rate"
    min: 1
    max: 20
    step: 1
    icon: "mdi:update"

automation:
- alias: set_hue_polling_interval
  trigger:
    platform: state
    entity_id: input_number.hue_polling_interval
  action:
  - service: fasthue.set_update_interval
    entity_id: sensor.hue_polling_interval
    data_template:
      scan_interval:
        seconds: '{{states("input_number.hue_polling_interval") | int}}'
```

The `scan_interval` field could also be expressed as a _timedelta string_, like `scan_interval: "00:00:{{states('input_number.hue_polling_interval') | int }}"`.

## Limitations

The modified `scan_interval` for the Hue bridge with this custom integration has a **lower limit of 1s**,
and that's _not only_ because at 1Hz the probability of generating errors in the bridge is high,
but also **because there is no way to do it faster** (if using the HA Core infrastructure to do the polling).

All internal schedulers in HA Core use its _internal clock_,
which is a periodic `EVENT_TIME_CHANGED`, **fired each second**.
So there is no point in setting an update interval of something less than 1s,
because it will be called at 1Hz tops, once for each `time_changed` event.

Also, `float` numbers like 1.5 have no sense for this,
and that's why the scan_interval is an integer,
and the minor unit in all 'time' fields along HA Core is the second :)
