# sensor.py
"""
Sensor-Definitionen und Berechnung der Raumklima-Werte
"""

from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ICONS, DEFAULT_TEXTS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RaumklimaSensor(entry, coordinator)])

class RaumklimaSensor(CoordinatorEntity, SensorEntity):
    """Sensor für Raumklima und Lüftungsempfehlung."""

    def __init__(self, entry: ConfigEntry, coordinator) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = f"Raumklimamonitor {entry.title}"
        self._attr_unique_id = f"raumklima_{entry.entry_id}"

    @property
    def native_value(self) -> str:
        return self._calculate_climate_status()

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "temperature_in": self._get_sensor_value("temperature_in"),
            "humidity_in": self._get_sensor_value("humidity_in"),
            "climate_status": self._calculate_climate_status(),
            "ventilation_recommendation": self._calculate_ventilation()
        }

    def _get_sensor_value(self, key: str) -> float:
        entity_id = self._entry.options.get(key)
        if not entity_id:
            return None
        state = self.hass.states.get(entity_id)
        try:
            return float(state.state)
        except (ValueError, TypeError, AttributeError):
            return None

    def _calculate_climate_status(self) -> str:
        temp = self._get_sensor_value("temperature_in")
        hum = self._get_sensor_value("humidity_in")
        if temp is None or hum is None:
            return "unbekannt"
        if 20 <= temp <= 24 and 40 <= hum <= 60:
            return self._entry.options.get("status_text_good", DEFAULT_TEXTS["good"])
        elif 18 <= temp < 26 and 30 <= hum < 70:
            return self._entry.options.get("status_text_ok", DEFAULT_TEXTS["ok"])
        else:
            return self._entry.options.get("status_text_bad", DEFAULT_TEXTS["bad"])

    def _calculate_ventilation(self) -> str:
        t_in = self._get_sensor_value("temperature_in")
        h_in = self._get_sensor_value("humidity_in")
        t_out = self._get_sensor_value("temperature_out")
        h_out = self._get_sensor_value("humidity_out")
        if None in (t_in, h_in, t_out, h_out):
            return "unbekannt"

        from math import log
        try:
            dp_in = (243.04 * (log(h_in / 100) + ((17.625 * t_in) / (243.04 + t_in)))) / \
                    (17.625 - log(h_in / 100) - ((17.625 * t_in) / (243.04 + t_in)))
            dp_out = (243.04 * (log(h_out / 100) + ((17.625 * t_out) / (243.04 + t_out)))) / \
                     (17.625 - log(h_out / 100) - ((17.625 * t_out) / (243.04 + t_out)))
            if dp_in - dp_out > 2:
                return "Lüften empfohlen"
            else:
                return "Kein Lüften nötig"
        except Exception as e:
            _LOGGER.warning(f"Fehler bei Lüftungsberechnung: {e}")
            return "unbekannt"
