"""Color definitions for the application."""

from dataclasses import dataclass


@dataclass
class Color:
    """Color constants used throughout the application."""

    # Main theme color
    MAIN: str = "#42f5b9"

    # Standard colors
    WHITE: str = "#ffffff"
    BLACK: str = "#000000"
    RED: str = "#ff0000"
    GREEN: str = "#42f5b9"  # Same as MAIN for consistency
    BLUE: str = "#1e88e5"
    YELLOW: str = "#ffff00"

    # UI colors
    BACKGROUND: str = "#2d2d2d"
    FOREGROUND: str = "#ffffff"
    ACCENT: str = "#42f5b9"  # Same as MAIN
    ERROR: str = "#ff5252"
    WARNING: str = "#ffb74d"
    SUCCESS: str = "#66bb6a"
