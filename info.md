# unifi_status
High level health status of UniFi Security Gateway devices via UniFi Controller

Connects to a Ubiquiti Controller instance to monitor high level health information on the setup including alerts and firmware updates

Switch is used to reboot the AP

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
