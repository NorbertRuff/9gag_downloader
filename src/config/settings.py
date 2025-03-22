"""Settings handler for the application.

This module provides functionality for saving and loading application settings.
"""

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from src.utils.logging import Logger


@dataclass
class AppSettings:
    """App settings data class to store user preferences."""

    # Remember source and destination paths
    last_source_file: str = ""
    last_destination_folder: str = ""

    # Remember checkboxes state
    saved_gags_selected: bool = False
    upvoted_gags_selected: bool = True

    # UI settings
    window_width: int = 1024
    window_height: int = 768

    # Remember last successful downloads
    recent_files: List[str] = field(default_factory=list)

    def update_recent_file(self, filepath: str) -> None:
        """Add a file to recent files or move it to the top if it already exists.

        Args:
            filepath: Path to the file to add.
        """
        # Remove if already exists (to move it to the top)
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)

        # Add to the beginning of the list
        self.recent_files.insert(0, filepath)

        # Keep only the last 5 files
        self.recent_files = self.recent_files[:5]


class SettingsManager:
    """Handler for loading and saving application settings."""

    def __init__(self, logger: Optional[Logger] = None):
        """Initialize the settings manager.

        Args:
            logger: Logger instance for logging messages.
        """
        self.logger = logger or Logger("SettingsManager")
        self.settings_file = self._get_settings_file_path()
        self.settings = self._load_settings()

    def _get_settings_file_path(self) -> Path:
        """Get the path to the settings file.

        Returns:
            Path to the settings file.
        """
        # Get app data directory
        if os.name == "nt":  # Windows
            app_data = Path(os.environ.get("APPDATA", ""))
        else:  # Linux/Mac
            app_data = Path.home() / ".config"

        # Create app directory if it doesn't exist
        app_dir = app_data / "9gag_downloader"
        app_dir.mkdir(parents=True, exist_ok=True)

        return app_dir / "settings.json"

    def _load_settings(self) -> AppSettings:
        """Load settings from file or create default settings.

        Returns:
            AppSettings object.
        """
        if not self.settings_file.exists():
            self.logger.info("Settings file not found, using defaults")
            return AppSettings()

        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Convert dict to AppSettings
            settings = AppSettings(
                last_source_file=data.get("last_source_file", ""),
                last_destination_folder=data.get("last_destination_folder", ""),
                saved_gags_selected=data.get("saved_gags_selected", False),
                upvoted_gags_selected=data.get("upvoted_gags_selected", True),
                window_width=data.get("window_width", 1024),
                window_height=data.get("window_height", 768),
                recent_files=data.get("recent_files", []),
            )

            self.logger.info(f"Settings loaded from {self.settings_file}")
            return settings

        except Exception as e:
            self.logger.error(f"Error loading settings: {str(e)}")
            return AppSettings()

    def save_settings(self) -> bool:
        """Save current settings to file.

        Returns:
            True if successful, False otherwise.
        """
        try:
            # Convert dataclass to dict
            data = asdict(self.settings)

            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            self.logger.error(f"Error saving settings: {str(e)}")
            return False

    def update_source_file(self, file_path: str) -> None:
        """Update the last source file path.

        Args:
            file_path: Path to the source file.
        """
        if file_path:
            self.settings.last_source_file = file_path
            self.settings.update_recent_file(file_path)
            self.save_settings()

    def update_destination_folder(self, folder_path: str) -> None:
        """Update the last destination folder path.

        Args:
            folder_path: Path to the destination folder.
        """
        if folder_path:
            self.settings.last_destination_folder = folder_path
            self.save_settings()

    def update_checkboxes(self, saved_selected: bool, upvoted_selected: bool) -> None:
        """Update checkbox selections.

        Args:
            saved_selected: Whether saved gags checkbox is selected.
            upvoted_selected: Whether upvoted gags checkbox is selected.
        """
        self.settings.saved_gags_selected = saved_selected
        self.settings.upvoted_gags_selected = upvoted_selected
        self.save_settings()

    def update_window_size(self, width: int, height: int) -> None:
        """Update window size.

        Args:
            width: Window width.
            height: Window height.
        """
        if width > 400 and height > 300:  # Sanity check
            self.settings.window_width = width
            self.settings.window_height = height
            self.save_settings()
