![Validate with hassfest](https://github.com/azogue/fasthue/workflows/Validate%20with%20hassfest/badge.svg?branch=master)
![HACS validation](https://github.com/azogue/fasthue/workflows/HACS%20validation/badge.svg?branch=master)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<br><a href="https://www.buymeacoffee.com/azogue" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-black.png" width="150px" height="35px" alt="Buy Me A Coffee" style="height: 35px !important;width: 150px !important;" ></a>

# Fast-Hue customizer

Custom integration to **modify the fixed update interval (5s)** of the main `hue` integration.

It is configured only by UI, and creates a sensor entity for each Hue bridge, showing the current polling interval.
It also register a new service **`fasthue.set_update_interval`** to be able to change the update interval dynamically, even from automations or scripts.

## Installation

Place the `custom_components` folder in your configuration directory
(or add its contents to an existing `custom_components` folder).

## Installation through HACS

The easiest way to install it.

Until added to the default list in [HACS](https://hacs.xyz/), it can be added as a **custom repository** by adding `https://github.com/azogue/fasthue` (with category: Integration).

## Configuration

Add it from the Integrations menu, set the desired new update interval, and you're good to go.

If there are more than 1 hue bridge, all of them will get the same update interval. Created sensors live under the Hue bridge device, as they are linked to each hub.

Once configured, the new `fasthue.set_update_interval` service is available to use with each bridge (:= sensor entity),
so different refresh intervals can be set for different bridges, and they can be changed anytime.

When the integration is removed, the sensor entities are deleted, the service dissapears,
and the update interval is set again to 5 seconds, like nothing happened,
so you can try it with no danger :)

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
