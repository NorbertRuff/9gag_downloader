"""Theme configuration for the application."""

from dataclasses import dataclass

from .colors import Color


@dataclass
class Theme:
    """UI theme configuration for the application."""

    # UI settings
    border_width: int = 1
    border_color: str = Color.BORDER
    padding: int = 6
    small_padding: int = 6
    large_padding: int = 20
    element_width: int = 1000

    # Spacing
    row_spacing: int = 10
    column_spacing: int = 10
    section_spacing: int = 20

    # Widget settings
    corner_radius: int = 8
    button_corner_radius: int = 6
    border_radius: int = 8

    # Window settings
    geometry: str = "1024x768"
    min_width: int = 1024
    min_height: int = 768
    title: str = "9GAG Downloader"

    # Theme settings
    appearance_mode: str = "dark"

    # Background colors
    main_bg: str = Color.BACKGROUND
    section_bg: str = Color.CARD_BG

    # Text settings
    font_family: str = "Segoe UI" if "win" in __import__("sys").platform else "Arial"
    header_font: tuple = (font_family, 16, "bold")
    title_font: tuple = (font_family, 14, "bold")
    normal_font: tuple = (font_family, 10)
    small_font: tuple = (font_family, 10)
    button_font: tuple = (font_family, 12, "bold")
    text_color: str = Color.FOREGROUND

    # Button settings
    button_color: str = Color.BUTTON_BG
    button_hover_color: str = Color.BUTTON_HOVER
    button_text_color: str = Color.BUTTON_TEXT
    button_disabled_color: str = Color.BUTTON_DISABLED
    button_height: int = 40
    main_button_height: int = 50
    button_width: int = 120
    main_button_width: int = 200

    # Cancel button settings
    button_cancel_color: str = Color.RED
    button_cancel_hover_color: str = "#c0392b"  # Darker red

    # Input settings
    entry_bg: str = Color.INPUT_BG
    entry_fg: str = Color.INPUT_TEXT
    entry_placeholder_color: str = Color.INPUT_PLACEHOLDER

    # Progress bar settings
    progress_color: str = Color.MAIN
    progress_background_color: str = Color.SECONDARY_BG
    progress_height: int = 20

    # Status colors
    info_color: str = Color.BLUE
    success_color: str = Color.SUCCESS
    error_color: str = Color.ERROR
    warning_color: str = Color.WARNING
