"""Theme configuration for the application."""

from dataclasses import dataclass

from .colors import Color


@dataclass
class Theme:
    """UI theme configuration for the application."""

    # UI settings
    border_width: int = 1
    border_color: str = Color.MAIN
    padding: int = 10
    element_width: int = 1000

    # Window settings
    geometry: str = "1024x768"
    min_width: int = 1024
    min_height: int = 768
    title: str = "9GAG Downloader"

    # Theme settings
    appearance_mode: str = "dark"

    # Button settings
    button_color: str = Color.MAIN
    button_hover_color: str = Color.BLUE
    button_text_color: str = Color.BLACK

    # Progress bar settings
    progress_color: str = Color.MAIN
    progress_background_color: str = Color.BACKGROUND
