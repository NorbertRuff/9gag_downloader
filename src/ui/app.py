"""Main application window class.

This class is the frame for the main window.
It contains all the subframes and the main application loop.
"""

import tkinter as tk
from typing import List, Optional

import customtkinter as ctk

from src.config import Color, Theme
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

    def __init__(self, downloader: DownloadHandler, theme: Theme, logger: Logger):
        """Initialize the application window.

        Args:
            downloader: Download handler for downloading gags.
            theme: Theme configuration.
            logger: Logger instance.
        """
        super().__init__()

        # Store dependencies
        self.downloader = downloader
        self.theme = theme
        self.logger = logger

        # Set up the UI
        self._setup_window()
        self._create_widgets()
        self._place_widgets()

    def _setup_window(self) -> None:
        """Configure the main window settings."""
        self.title(self.theme.title)
        self.geometry(self.theme.geometry)
        self.minsize(self.theme.min_width, self.theme.min_height)

        # Set appearance mode
        ctk.set_appearance_mode(self.theme.appearance_mode)

        # Configure grid
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _create_widgets(self) -> None:
        """Create all the UI widgets."""
        # App title
        self.title_label = ctk.CTkLabel(
            self, text="9GAG Downloader", font=("Arial", 20)
        )

        # Create frames
        self.header = HeaderFrame(self, theme=self.theme)
        self.checkboxes_frame = CheckboxesFrame(self, theme=self.theme)
        self.source_frame = SourceFileFrame(self, theme=self.theme)
        self.destination_frame = DestinationFolderFrame(self, theme=self.theme)
        self.progress_frame = ProgressBarFrame(self, theme=self.theme)
        self.download_frame = DownloadFrame(
            self, theme=self.theme, start_download_callback=self.start_download_progress
        )

    def _place_widgets(self) -> None:
        """Place all widgets in the grid."""
        # Place app title
        self.title_label.grid(
            row=0, column=0, columnspan=2, sticky=tk.W + tk.E, padx=10, pady=10
        )

        # Place frames
        self.header.grid(
            row=1, column=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5
        )
        self.checkboxes_frame.grid(
            row=1, column=1, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5
        )
        self.source_frame.grid(
            row=2, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5
        )
        self.destination_frame.grid(
            row=3, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5
        )
        self.download_frame.grid(
            row=4, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5
        )

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

        # Download statistics
        successful = 0
        failed = 0

        # Download each gag
        for i, gag in enumerate(gags):
            # Update progress
            progress_percent = i / one_percent / 100
            progress_int = int(i / one_percent)
            self.progress_frame.set_progress_bar(
                progress_percent, progress_int, color=Color.MAIN
            )

            # Update status message
            self.set_progress_message(
                f"Downloading gag: {gag.title} ({i + 1}/{total_gags})",
                color=Color.SUCCESS,
            )

            # Process UI events
            self.update()

            # Download the gag
            if self.downloader.download_gag(gag, destination_folder):
                successful += 1
            else:
                failed += 1

        # Update progress to complete
        self.progress_frame.set_progress_bar(1.0, 100, color=Color.SUCCESS)

        # Show final status
        if failed > 0:
            self.set_progress_message(
                f"Download finished: {successful} successful, {failed} failed",
                color=Color.WARNING if failed > 0 else Color.SUCCESS,
            )
        else:
            self.set_progress_message(
                f"All {successful} gags downloaded successfully!", color=Color.SUCCESS
            )

        # Enable UI elements
        self.download_frame.enable_download_button()
        self.progress_frame.pack_open_log_button()
        self.update()

    def set_progress_message(self, text: str, color: str = Color.WHITE) -> None:
        """Set the progress message displayed to the user.

        Args:
            text: Message text to display.
            color: Text color.
        """
        self.download_frame.set_progress_message(text=text, color=color)
