# __init__.py
"""
Initialisierungsdatei für das Raumklimamonitor-Plugin
"""

from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Initialisierung des Raumklimamonitor-Plugins"""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: dict) -> bool:
    """Setup für Konfigurationseintrag"""
    hass.data[DOMAIN][entry.entry_id] = entry
    return True
