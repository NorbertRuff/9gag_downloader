"""Tests for the settings manager module."""

import json
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.config import AppSettings, SettingsManager


class TestSettingsManager(unittest.TestCase):
    """Test cases for the settings manager."""

    def setUp(self):
        """Set up the test case."""
        # Create a temp directory for test settings
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_config_dir = os.path.join(current_dir, "test_config")
        os.makedirs(self.test_config_dir, exist_ok=True)

        # Set up mock logger
        self.mock_logger = MagicMock()

        # Create test settings file path
        self.test_settings_path = Path(
            os.path.join(self.test_config_dir, "test_settings.json")
        )

    def tearDown(self):
        """Clean up after the test."""
        # Clean up test files
        if Path(self.test_config_dir).exists():
            import shutil

            shutil.rmtree(self.test_config_dir)

    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_save_and_load_settings(self, mock_get_path):
        """Test saving and loading settings."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Modify settings
        manager.settings.window_width = 1200
        manager.settings.window_height = 800
        manager.settings.last_source_file = "/test/source.html"
        manager.settings.last_destination_folder = "/test/destination"
        manager.settings.saved_gags_selected = True
        manager.settings.upvoted_gags_selected = False
        manager.settings.recent_files = ["/test/file1.html", "/test/file2.html"]

        # Save settings
        manager.save_settings()

        # Create a new manager to load the settings
        new_manager = SettingsManager(self.mock_logger)

        # Verify settings were loaded correctly
        self.assertEqual(new_manager.settings.window_width, 1200)
        self.assertEqual(new_manager.settings.window_height, 800)
        self.assertEqual(new_manager.settings.last_source_file, "/test/source.html")
        self.assertEqual(
            new_manager.settings.last_destination_folder, "/test/destination"
        )
        self.assertTrue(new_manager.settings.saved_gags_selected)
        self.assertFalse(new_manager.settings.upvoted_gags_selected)
        self.assertEqual(
            new_manager.settings.recent_files, ["/test/file1.html", "/test/file2.html"]
        )

    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_update_source_file(self, mock_get_path):
        """Test updating the source file."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Update source file
        manager.update_source_file("/test/updated_source.html")

        # Verify settings were updated
        self.assertEqual(manager.settings.last_source_file, "/test/updated_source.html")
        self.assertIn("/test/updated_source.html", manager.settings.recent_files)

        # Verify the file was saved
        self.assertTrue(Path(self.test_settings_path).exists())

    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_update_destination_folder(self, mock_get_path):
        """Test updating the destination folder."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Update destination folder
        manager.update_destination_folder("/test/updated_destination")

        # Verify settings were updated
        self.assertEqual(
            manager.settings.last_destination_folder, "/test/updated_destination"
        )

        # Verify the file was saved
        self.assertTrue(Path(self.test_settings_path).exists())

    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_update_checkboxes(self, mock_get_path):
        """Test updating the checkboxes."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Update checkboxes
        manager.update_checkboxes(True, False)

        # Verify settings were updated
        self.assertTrue(manager.settings.saved_gags_selected)
        self.assertFalse(manager.settings.upvoted_gags_selected)

        # Verify the file was saved
        self.assertTrue(Path(self.test_settings_path).exists())

    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_update_window_size(self, mock_get_path):
        """Test updating the window size."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Update window size
        manager.update_window_size(1500, 900)

        # Verify settings were updated
        self.assertEqual(manager.settings.window_width, 1500)
        self.assertEqual(manager.settings.window_height, 900)

        # Verify the file was saved
        self.assertTrue(Path(self.test_settings_path).exists())

    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_recent_files_limit(self, mock_get_path):
        """Test that recent files are limited to 5."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Add 7 files (more than the limit)
        for i in range(7):
            manager.update_source_file(f"/test/file{i}.html")

        # Verify only the 5 most recent files are kept
        self.assertEqual(len(manager.settings.recent_files), 5)
        self.assertEqual(manager.settings.recent_files[0], "/test/file6.html")
        self.assertEqual(manager.settings.recent_files[4], "/test/file2.html")

    @patch("src.config.settings.Path.exists")
    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_load_nonexistent_file(self, mock_get_path, mock_exists):
        """Test loading settings when file doesn't exist."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Mock Path.exists to return False
        mock_exists.return_value = False

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Verify default settings were used
        self.assertEqual(manager.settings.window_width, 1024)
        self.assertEqual(manager.settings.window_height, 768)
        self.assertEqual(manager.settings.last_source_file, "")
        self.assertEqual(manager.settings.last_destination_folder, "")
        self.assertFalse(manager.settings.saved_gags_selected)
        self.assertTrue(manager.settings.upvoted_gags_selected)
        self.assertEqual(manager.settings.recent_files, [])

    @patch("src.config.settings.SettingsManager._get_settings_file_path")
    def test_corrupt_settings_file(self, mock_get_path):
        """Test loading settings when file is corrupt."""
        # Mock the settings file path
        mock_get_path.return_value = self.test_settings_path

        # Create a corrupt settings file
        with open(self.test_settings_path, "w") as f:
            f.write("This is not valid JSON")

        # Create a settings manager
        manager = SettingsManager(self.mock_logger)

        # Verify default settings were used
        self.assertEqual(manager.settings.window_width, 1024)
        self.assertEqual(manager.settings.window_height, 768)
        self.assertEqual(manager.settings.last_source_file, "")
        self.assertEqual(manager.settings.last_destination_folder, "")
        self.assertFalse(manager.settings.saved_gags_selected)
        self.assertTrue(manager.settings.upvoted_gags_selected)
        self.assertEqual(manager.settings.recent_files, [])


if __name__ == "__main__":
    unittest.main()
