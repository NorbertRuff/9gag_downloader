"""Main application window class.

This class is the frame for the main window.
It contains all the subframes and the main application loop.
"""

import tkinter as tk
from typing import List, Optional
from pathlib import Path

import customtkinter as ctk

from src.config import Color, Theme, SettingsManager
from src.core.downloader import DownloadHandler
from src.core.models import Gag
from src.core.parser import HtmlParser
from src.ui.frames import (
    CheckboxesFrame,
    DestinationFolderFrame,
    DownloadFrame,
    HeaderFrame,
    ProgressBarFrame,
    SourceFileFrame,
)
from src.utils.helpers import create_dirs_if_not_exist
from src.utils.logging import Logger


class App(ctk.CTk):
    """Main application window."""

    def __init__(
        self,
        downloader: DownloadHandler,
        theme: Theme,
        logger: Logger,
        settings_manager: SettingsManager,
    ):
        """Initialize the application window.

        Args:
            downloader: Download handler for downloading gags.
            theme: Theme configuration.
            logger: Logger instance.
            settings_manager: Settings manager for persisting user preferences.
        """
        super().__init__()
        self.downloader = downloader
        self.theme = theme
        self.logger = logger
        self.settings_manager = settings_manager

        # Set up the UI
        self._setup_window()
        self._create_widgets()
        self._place_widgets()

        # Apply saved settings
        self._apply_saved_settings()

        # Bind events for saving settings
        self._bind_events()

    def _setup_window(self) -> None:
        """Configure the main window settings."""
        self.title(self.theme.title)

        # Get window size from settings
        settings = self.settings_manager.settings
        geometry = f"{settings.window_width}x{settings.window_height}"
        self.geometry(geometry)

        self.minsize(self.theme.min_width, self.theme.min_height)

        # Set background color
        self.configure(fg_color=self.theme.main_bg)

        # Set appearance mode
        ctk.set_appearance_mode(self.theme.appearance_mode)

        # Configure grid with better spacing
        self.grid_rowconfigure(0, weight=1)  # Main content
        self.grid_columnconfigure(0, weight=1)  # Full width

    def _create_widgets(self) -> None:
        """Create all the UI widgets."""
        # Create main container frame
        self.main_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )

        # Create frames
        self.header = HeaderFrame(
            self.main_container,
            theme=self.theme,
            corner_radius=self.theme.corner_radius,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
            fg_color=self.theme.section_bg,
        )

        self.checkboxes_frame = CheckboxesFrame(
            self.main_container,
            theme=self.theme,
            corner_radius=self.theme.corner_radius,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
            fg_color=self.theme.section_bg,
        )

        self.source_frame = SourceFileFrame(
            self.main_container,
            theme=self.theme,
            corner_radius=self.theme.corner_radius,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
            fg_color=self.theme.section_bg,
            recent_files=self.settings_manager.settings.recent_files,
        )

        self.destination_frame = DestinationFolderFrame(
            self.main_container,
            theme=self.theme,
            corner_radius=self.theme.corner_radius,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
            fg_color=self.theme.section_bg,
        )

        self.progress_frame = ProgressBarFrame(
            self.main_container,
            theme=self.theme,
            corner_radius=self.theme.corner_radius,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
            fg_color=self.theme.section_bg,
        )

        self.download_frame = DownloadFrame(
            self.main_container,
            theme=self.theme,
            corner_radius=self.theme.corner_radius,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
            fg_color=self.theme.section_bg,
            start_download_callback=self.start_download_progress,
        )

    def _apply_saved_settings(self) -> None:
        """Apply saved settings from previous sessions."""
        settings = self.settings_manager.settings

        # Apply source file
        if settings.last_source_file and Path(settings.last_source_file).exists():
            self.source_frame.set_entry_value(settings.last_source_file)

        # Apply destination folder
        if (
            settings.last_destination_folder
            and Path(settings.last_destination_folder).exists()
        ):
            self.destination_frame.set_entry_value(settings.last_destination_folder)

        # Apply checkbox settings
        self.checkboxes_frame.set_saved_gags_var(settings.saved_gags_selected)
        self.checkboxes_frame.set_upvoted_gags_var(settings.upvoted_gags_selected)

    def _bind_events(self) -> None:
        """Bind events for saving settings."""
        # Bind window resize event
        self.bind("<Configure>", self._on_window_configure)

        # Bind source file changes
        self.source_frame.set_file_changed_callback(self._on_source_file_changed)

        # Bind destination folder changes
        self.destination_frame.set_folder_changed_callback(
            self._on_destination_folder_changed
        )

        # Bind checkbox changes
        self.checkboxes_frame.set_checkbox_changed_callback(self._on_checkbox_changed)

    def _on_window_configure(self, event: tk.Event) -> None:
        """Handle window resize events.

        Args:
            event: Configure event.
        """
        # Only process events from the main window
        if event.widget == self:
            # Avoid saving during initialization or when minimized
            if event.width > 100 and event.height > 100:
                self.settings_manager.update_window_size(event.width, event.height)

    def _on_source_file_changed(self, file_path: str) -> None:
        """Handle source file change.

        Args:
            file_path: New source file path.
        """
        if file_path:
            self.settings_manager.update_source_file(file_path)

    def _on_destination_folder_changed(self, folder_path: str) -> None:
        """Handle destination folder change.

        Args:
            folder_path: New destination folder path.
        """
        if folder_path:
            self.settings_manager.update_destination_folder(folder_path)

    def _on_checkbox_changed(
        self, saved_selected: bool, upvoted_selected: bool
    ) -> None:
        """Handle checkbox state changes.

        Args:
            saved_selected: Whether saved gags checkbox is selected.
            upvoted_selected: Whether upvoted gags checkbox is selected.
        """
        self.settings_manager.update_checkboxes(saved_selected, upvoted_selected)

    def _place_widgets(self) -> None:
        """Place all widgets in the grid."""
        # Place main container
        self.main_container.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=self.theme.padding,
            pady=self.theme.padding,
        )

        # Configure main container grid
        self.main_container.grid_columnconfigure(0, weight=1)  # Main content column
        self.main_container.grid_rowconfigure(0, weight=0)  # Header row
        self.main_container.grid_rowconfigure(1, weight=0)  # Checkboxes row
        self.main_container.grid_rowconfigure(2, weight=0)  # Source row
        self.main_container.grid_rowconfigure(3, weight=0)  # Destination row
        self.main_container.grid_rowconfigure(4, weight=0)  # Download row

        row = 0
        # Place frames
        self.header.grid(
            row=row,
            column=0,
            sticky=tk.NSEW,
            padx=self.theme.padding,
            pady=self.theme.padding,
        )

        row += 1
        self.checkboxes_frame.grid(
            row=row,
            column=0,
            sticky=tk.NSEW,
            padx=self.theme.padding,
            pady=self.theme.padding,
        )

        row += 1
        self.source_frame.grid(
            row=row,
            column=0,
            sticky=tk.NSEW,
            padx=self.theme.padding,
            pady=self.theme.padding,
        )

        row += 1
        self.destination_frame.grid(
            row=row,
            column=0,
            sticky=tk.NSEW,
            padx=self.theme.padding,
            pady=self.theme.padding,
        )

        row += 1
        self.download_frame.grid(
            row=row,
            column=0,
            sticky=tk.NSEW,
            padx=self.theme.padding,
            pady=self.theme.padding,
        )

        # Progress frame is initially hidden
        # It will be shown when needed

    def start_download_progress(self) -> None:
        """Start the download process based on user input."""
        # Get user inputs
        source_file = self.source_frame.get_entry_value()
        destination_folder = self.destination_frame.get_entry_value()
        saved_gags_check = self.checkboxes_frame.get_saved_gags_var()
        upvoted_gags_check = self.checkboxes_frame.get_upvoted_gags_var()

        # Validate inputs
        if not source_file:
            self.set_progress_message("Please select a source file.", color=Color.ERROR)
            return

        if not destination_folder:
            self.set_progress_message(
                "Please select a destination folder.", color=Color.ERROR
            )
            return

        if not saved_gags_check and not upvoted_gags_check:
            self.set_progress_message(
                "Please select at least one option.", color=Color.ERROR
            )
            return

        # Parse gags from the source file
        gags = self._parse_gags(source_file, upvoted_gags_check, saved_gags_check)
        if not gags:
            self.logger.error("No upvoted or saved gags found")
            self.set_progress_message(
                text="No upvoted or saved gags found", color=Color.ERROR
            )
            return

        # Show progress bar
        self.progress_frame.grid(
            row=5, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5
        )

        # Ensure download directories exist
        create_dirs_if_not_exist(destination_folder)

        # Download each gag
        self._process_downloads(gags, destination_folder)

    def _parse_gags(
        self, source_file: str, upvoted_gags: bool, saved_gags: bool
    ) -> Optional[List[Gag]]:
        """Parse gags from the source file.

        Args:
            source_file: Path to the source HTML file.
            upvoted_gags: Whether to include upvoted gags.
            saved_gags: Whether to include saved gags.

        Returns:
            List of gags or None if parsing failed.
        """
        try:
            return HtmlParser.parse_file(
                source_file, upvoted_gags=upvoted_gags, saved_gags=saved_gags
            )
        except FileNotFoundError:
            self.logger.error("9GAG data file not found")
            self.set_progress_message(
                text="9GAG data file not found", color=Color.ERROR
            )
            return None
        except Exception as e:
            self.logger.error(f"Error parsing file: {str(e)}")
            self.set_progress_message(
                text=f"Error parsing file: {str(e)}", color=Color.ERROR
            )
            return None

    def _process_downloads(self, gags: List[Gag], destination_folder: str) -> None:
        """Process and download all gags.

        Args:
            gags: List of gags to download.
            destination_folder: Folder to save downloads in.
        """
        total_gags = len(gags)
        one_percent = total_gags / 100 if total_gags > 0 else 1

        # Reset and initialize progress bar stats
        self.progress_frame.reset_stats()
        self.progress_frame.set_total_items(total_gags)

        # Download statistics
        successful = 0
        failed = 0
        already_downloaded = 0

        # For time estimate calculation
        import time

        start_time = time.time()

        # Download each gag
        for i, gag in enumerate(gags):
            # Check if download was canceled
            if self.progress_frame.is_download_cancelled():
                self.set_progress_message(
                    f"Download canceled: {successful} successful, {failed} failed, {already_downloaded} already downloaded",
                    color=Color.WARNING,
                )
                break

            # Update current item
            self.progress_frame.update_current_item(gag.title, i)

            # Update progress
            progress_percent = i / one_percent / 100
            progress_int = int(i / one_percent)

            # Calculate estimated time remaining
            elapsed = time.time() - start_time
            if i > 0:
                items_per_second = i / elapsed if elapsed > 0 else 0
                remaining_items = total_gags - i
                if items_per_second > 0:
                    remaining_seconds = remaining_items / items_per_second
                    minutes = int(remaining_seconds // 60)
                    seconds = int(remaining_seconds % 60)
                    remaining_time = f"{minutes:02d}:{seconds:02d}"
                else:
                    remaining_time = "--:--"
            else:
                remaining_time = "--:--"

            self.progress_frame.set_progress_bar(
                progress_percent,
                progress_int,
                color=Color.MAIN,
                remaining_time=remaining_time,
            )

            # Update status message
            self.set_progress_message(
                f"Downloading gag: {gag.title} ({i + 1}/{total_gags})",
                color=Color.SUCCESS,
            )

            # Process UI events
            self.update()

            # Detect if file already exists
            is_cached = False
            image_path = (
                Path(destination_folder)
                / "gags/images"
                / f"{self._sanitize_filename(gag.title)}.jpg"
            )
            video_path = (
                Path(destination_folder)
                / "gags/videos"
                / f"{self._sanitize_filename(gag.title)}.mp4"
            )

            if image_path.exists() or video_path.exists():
                is_cached = True
                is_video = video_path.exists()
                already_downloaded += 1
                self.progress_frame.increment_counters(cached=True, is_video=is_video)
                self.progress_frame.update_current_item(
                    gag.title, i, is_video=is_video, is_cached=True
                )
                successful += 1
                continue

            # Download the gag
            # First, try as video (our downloader tries video first, then image)
            download_result = self.downloader.download_gag(gag, destination_folder)

            if download_result:
                successful += 1
                self.progress_frame.increment_counters(
                    success=True, is_video=gag.is_video
                )
                self.progress_frame.update_current_item(
                    gag.title, i, is_video=gag.is_video
                )
                self.logger.info(
                    f"Downloaded as {'video' if gag.is_video else 'image'}: {gag.title}"
                )
            else:
                failed += 1
                self.progress_frame.increment_counters(failure=True)

        # Update progress to complete
        self.progress_frame.set_progress_bar(1.0, 100, color=Color.SUCCESS)

        # Show final status
        if failed > 0 or self.progress_frame.is_download_cancelled():
            status_color = Color.WARNING
        else:
            status_color = Color.SUCCESS

        # Final message takes into account already downloaded files
        if already_downloaded > 0:
            self.set_progress_message(
                f"Download finished: {successful} successful ({already_downloaded} already downloaded), {failed} failed",
                color=status_color,
            )
        else:
            self.set_progress_message(
                f"Download finished: {successful} successful, {failed} failed",
                color=status_color,
            )

        # Enable UI elements
        self.download_frame.enable_download_button()
        self.progress_frame.pack_open_log_button()
        self.update()

    def _sanitize_filename(self, title: str) -> str:
        """Sanitize a title for use in filenames.

        Args:
            title: Title to sanitize.

        Returns:
            Sanitized title.
        """
        import re

        sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
        return sanitized[:100]  # Limit length to 100 chars

    def set_progress_message(self, text: str, color: str = Color.WHITE) -> None:
        """Set the progress message displayed to the user.

        Args:
            text: Message text to display.
            color: Text color.
        """
        self.download_frame.set_progress_message(text=text, color=color)
