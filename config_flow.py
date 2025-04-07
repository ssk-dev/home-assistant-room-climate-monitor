# config_flow.py
"""
Konfigurationsfluss für das Raumklimamonitor-Plugin
"""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_DEVICE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
import homeassistant.helpers.entity_registry as er

from .const import DOMAIN, DEFAULT_TEXTS, ICONS

class RaumklimaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfigurationsflow für das Raumklimamonitor-Plugin."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=self._get_user_schema())

        # Speichern der Konfiguration, wenn alles passt
        self._save_entry(user_input)
        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

    def _get_user_schema(self):
        """Eingabefelder für den Konfigurationsschritt"""
        return vol.Schema({
            vol.Required(CONF_NAME, default="Wohnzimmer"): str,
            vol.Required(CONF_DEVICE_ID): str,
            vol.Optional("temperature_in", default=None): str,
            vol.Optional("humidity_in", default=None): str,
            vol.Optional("temperature_out", default=None): str,
            vol.Optional("humidity_out", default=None): str,
            vol.Optional("status_text_good", default=DEFAULT_TEXTS["good"]): str,
            vol.Optional("status_text_ok", default=DEFAULT_TEXTS["ok"]): str,
            vol.Optional("status_text_bad", default=DEFAULT_TEXTS["bad"]): str,
            vol.Optional("icon_good", default=ICONS["good"]): str,
            vol.Optional("icon_ok", default=ICONS["ok"]): str,
            vol.Optional("icon_bad", default=ICONS["bad"]): str,
        })

    def _save_entry(self, user_input):
        # Konfiguration speichern
        self.hass.data[DOMAIN] = {"user_input": user_input}
        self.context[CONF_NAME] = user_input[CONF_NAME]
        self.context[CONF_DEVICE_ID] = user_input[CONF_DEVICE_ID]
        self.context["options"] = user_input
