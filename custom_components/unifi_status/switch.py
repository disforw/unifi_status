"""
Support for Unifi Status Units
"""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_VERIFY_SSL,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
)

from . import DOMAIN, PLATFORMS, __version__

from .const import (
    CONF_SITE_ID,
    CONF_UNIFI_VERSION,
    DEFAULT_NAME,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_UNIFI_VERSION,
    DEFAULT_SITE,
    DEFAULT_VERIFY_SSL,
    MIN_TIME_BETWEEN_UPDATES,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_SITE_ID, default=DEFAULT_SITE): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Optional(CONF_UNIFI_VERSION, default=DEFAULT_UNIFI_VERSION): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): vol.Any(
            cv.boolean, cv.isfile
        ),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Unifi switch."""
    from pyunifi.controller import Controller, APIError

    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    site_id = config.get(CONF_SITE_ID)
    version = config.get(CONF_UNIFI_VERSION)
    port = config.get(CONF_PORT)
    verify_ssl = config.get(CONF_VERIFY_SSL)

    try:
        ctrl = Controller(
            host,
            username,
            password,
            port,
            version,
            site_id=site_id,
            ssl_verify=verify_ssl,
        )
    except APIError as ex:
        _LOGGER.error(f"Setup | Failed to connect to Unifi Conroler: {ex}")
        return False

    try:
        aps = ctrl.get_aps()
    except APIError as ex:
        _LOGGER.error(f"Setup | Failed to scan aps: {ex}")
    else:
        for device in aps:
            switch = device["name"].lower()
            add_entities([UnifiStatusSwitch(hass, ctrl, name, switch)], True)


class UnifiStatusSwitch(SwitchEntity):
    """Implementation of a UniFi Status switch."""

    def __init__(self, hass, ctrl, name, switch):
        """Initialize the switch."""
        self._hass = hass
        self._ctrl = ctrl
        self._name = name + " " + switch
        self._switch = switch
        self._mac = None
        self._state = STATE_UNKNOWN
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def available(self):
        """Return the availability of this switch."""
        _LOGGER.debug(f"[{self._name}] State: {self._state}")
        return self._state is not None

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        if self._mac:
            self._ctrl.restart_ap(self._mac)
            self._state = STATE_ON

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._state = STATE_OFF

    @property
    def state_attributes(self):
        """Return the device state attributes."""
        return self._attributes

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Set up the switch."""
        from pyunifi.controller import APIError

        try:
            aps = self._ctrl.get_aps()
        except APIError as ex:
            _LOGGER.error(f"Update | Failed to scan aps: {ex}")
        else:
            for device in aps:
                if self._switch == device["name"].lower():
                    self._attributes["model"] = device["model"]
                    self._attributes["serial"] = device["serial"]
                    self._attributes["version"] = device["version"]
                    self._attributes["ip"] = device["ip"]
                    self._attributes["mac"] = device["mac"]
                    self._mac = device["mac"]
                    self._attributes["uptime"] = device["uptime"]
                    self._state = STATE_OFF
