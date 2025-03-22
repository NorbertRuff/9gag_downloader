"""Configuration for the application."""

from .colors import Color
from .settings import AppSettings, SettingsManager
from .theme import Theme

__all__ = ["Color", "Theme", "AppSettings", "SettingsManager"]
