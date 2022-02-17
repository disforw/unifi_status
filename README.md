# unifi_status
High level health status of UniFi Security Gateway devices via UniFi Controller

Connects to a Ubiquiti Controller instance to monitor high level health information on the setup including alerts and firmware updates

## Installation
*__Manual mode__*

Place the `unifi_status` folder into your `custom_components` folder.

*__Adding custom repository to [HACS](https://hacs.xyz/)__*

Go to the Integrations page in HACS and select the three dots in the top right corner. Select Custom repositories.
Add repository url. Category - Integration. Read more on https://hacs.xyz/docs/faq/custom_repositories.

**Example configuration.yaml:**

```yaml
# Example configuration.yaml entry
sensor:
  - platform: unifi_status
    host: unifi
    username: username
    password: password
    monitored_conditions:
      - www
      - wlan
      - alerts
      - firmware

switch:
  - platform: unifi_status
    host: unifi
    username: username
    password: password
```
### Configuration Variables

**username**

  (string)(Required) A user on the controller

**password**

(string)(Required) The password for the account

**host**

  (string)(Optional) The hostname or IP address of your controller
  Default value: localhost

**port**

  (integer)(Optional) The port of your controller's web interface - this differs deopending on version - use 443 for UDMP-unifiOS
  Default value: 8443

**version**

  (string)(Optional) Can also  be set to 'v4' or 'UDMP-unifiOS'
  Default value: v5

**site_id**

  (string)(Optional) For multisite installations, you can specify site_id to specify which is used
  Default value: default

**verify_ssl**

  (boolean or filename)(Optional) Whether to do strict validation on SSL certificates of the Unifi controller. This can be true/false or the path to a locally trusted certificate to use for verification.
  Default value: false

**monitored_conditions**

  (list)(Optional) A list of the sensors to monitor
  Default value: If not defined all sensors are setup

### Monitored Conditions

The following sensors can be monitored

**vpn**

  The status of the VPN sub-system

**www**

  The status of the WWW sub-system
  Attribute data includes speedtest results

**lan**

  The status of the LAN sub-system
  Attribute data includes the IP of the USG

**wan**

  The status of the WAN sub-system
  Attribute data includes the WAN IP (e.g. dynamic IP as allocated by your ISP)

**wlan**

  The status of the Wifi Access Points
  Attribute data includes number of guests

**alerts**

  The number of unarchived alerts on the controller
  Attribute data lists the detail of each alert

**firmware**

  The number of devices that are available for a firmware update.
  Attribute data lists the friendly name of the relvant devices.


Switch is used to restart the AP.


### In Development - Notes

The sensor currently accesses the controller everytime an individual sensor is updated. This should be optimised to access once and then feed data to the other appropriate sensors to reduce overhead.
