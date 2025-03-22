"""Color definitions for the application."""

from dataclasses import dataclass


@dataclass
class Color:
    """Color constants used throughout the application."""

    # Main theme color
    MAIN: str = "#42f5b9"  # Original teal color

    # Standard colors
    WHITE: str = "#ffffff"
    BLACK: str = "#1e1e1e"  # Softer black
    RED: str = "#e74c3c"  # Softer red
    GREEN: str = "#42f5b9"  # Same as MAIN for consistency
    BLUE: str = "#1e88e5"  # Original blue color
    YELLOW: str = "#f1c40f"  # Softer yellow

    # UI colors
    BACKGROUND: str = "#252525"  # Dark background
    SECONDARY_BG: str = "#333333"  # Slightly lighter background for contrast
    CARD_BG: str = "#2d2d2d"  # Card/panel background
    FOREGROUND: str = "#f5f5f5"  # Light text
    ACCENT: str = "#42f5b9"  # Same as MAIN
    ERROR: str = "#e74c3c"  # Error messages
    WARNING: str = "#f39c12"  # Warning messages
    SUCCESS: str = "#42f5b9"  # Success messages (using main teal)

    # Button colors
    BUTTON_BG: str = "#42f5b9"  # Button background (teal)
    BUTTON_HOVER: str = "#32d5a9"  # Button hover (darker teal)
    BUTTON_TEXT: str = "#1e1e1e"  # Button text (dark for better contrast with teal)
    BUTTON_DISABLED: str = "#95a5a6"  # Disabled button

    # Border colors
    BORDER: str = "#404040"  # Subtle border color

    # Input field colors
    INPUT_BG: str = "#333333"
    INPUT_TEXT: str = "#eeeeee"
    INPUT_PLACEHOLDER: str = "#7f8c8d"
