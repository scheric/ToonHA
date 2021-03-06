"""
Toon van Eneco Thermostat Support.

This provides a component for the rebranded Quby thermostat as provided by
Eneco.
"""

import logging
from homeassistant.components.climate.const import (STATE_AUTO,
                                              STATE_HEAT,
                                              STATE_ECO,
                                              STATE_COOL,
                                              SUPPORT_TARGET_TEMPERATURE,
                                              SUPPORT_OPERATION_MODE)
from homeassistant.const import (TEMP_CELSIUS, STATE_OFF, ATTR_TEMPERATURE)
from homeassistant.components.climate import ClimateDevice

import custom_components.toon as toon_main

_LOGGER = logging.getLogger(__name__)
SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE

HA_TOON = {
                  STATE_AUTO: 'Comfort',
                  STATE_HEAT: 'Home',
                  STATE_ECO: 'Away',
                  STATE_COOL: 'Sleep'
                 }

TOON_HA = {value: key for key, value in HA_TOON.items()}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup thermostat."""
    # Add toon
    add_devices((ThermostatDevice(hass), ), True)

class ThermostatDevice(ClimateDevice):
    """Interface class for the toon module and HA."""

    def __init__(self, hass):
        """Initialize the device."""
        self._name = 'Toon van Eneco'
        self.hass = hass
        self.thermos = hass.data[toon_main.TOON_HANDLE]

        # set up internal state vars
        self._state = None
        self._temperature = None
        self._setpoint = None
        self._operation_list = [STATE_AUTO,
                                STATE_HEAT,
                                STATE_ECO,
                                STATE_COOL,
                                STATE_OFF]

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS
                                   
    @property
    def name(self):
        """Name of this Thermostat."""
        return self._name

    @property
    def should_poll(self):
        """Polling is required."""
        return True

    @property
    def temperature_unit(self):
        """The unit of measurement used by the platform."""
        return TEMP_CELSIUS

    @property
    def current_operation(self):
        """Return current operation i.e. comfort, home, away."""
        if TOON_HA.get(self.thermos.get_data('state')) == None:
            return STATE_OFF
        else: 
            return TOON_HA.get(self.thermos.get_data('state'))

    @property
    def operation_list(self):
        """List of available operation modes."""
        return self._operation_list

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.thermos.get_data('temp')

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self.thermos.get_data('setpoint')

    def set_temperature(self, **kwargs):
        """Change the setpoint of the thermostat."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        self.thermos.set_temp(temp)

    def set_operation_mode(self, operation_mode):
        """Set new operation mode as toonlib requires it."""
        self.thermos.set_state(HA_TOON[operation_mode])

    def update(self):
        """Update local state."""
        self.thermos.update()
