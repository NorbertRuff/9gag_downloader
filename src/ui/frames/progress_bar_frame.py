"""Progress bar frame for displaying download progress.

This frame shows a progress bar and percentage to track the download progress.
"""

import tkinter as tk
from typing import Any, Dict, Optional

import customtkinter as ctk

from src.config import Color, Theme
from src.utils.logging import Logger


class ProgressBarFrame(ctk.CTkFrame):
    """Frame containing a progress bar and percentage indicator."""

    def __init__(self, master: Any, theme: Theme, **kwargs: Dict[str, Any]):
        """Initialize the progress bar frame.

        Args:
            master: Parent widget.
            theme: Theme configuration.
            **kwargs: Additional keyword arguments to pass to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.theme = theme
        self.logger_instance = Logger("9GAG Downloader")
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and place the widgets in the frame."""
        # Create progress frame
        self.progress_frame = ctk.CTkFrame(
            self,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
        )

        # Create progress label
        ctk.CTkLabel(
            self.progress_frame, text="Progress:", font=("Arial", 12, "bold")
        ).pack(padx=self.theme.padding, pady=self.theme.padding, side=tk.LEFT)

        # Create progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            progress_color=self.theme.progress_color,
            height=25,
            width=self.theme.element_width,
        )
        self.progress_bar.set(0)  # Initialize to 0

        # Create percentage label
        self.progress_bar_percentage = ctk.CTkLabel(
            self.progress_frame, text="0%", font=("Arial", 20)
        )

        # Create open log button (initially hidden)
        self.open_log_button = ctk.CTkButton(
            self.progress_frame,
            text="Open Log",
            width=150,
            height=40,
            font=("Arial", 12),
            command=self._open_log,
        )

        # Pack widgets
        self.progress_bar_percentage.pack(
            padx=self.theme.padding, pady=self.theme.padding, side=tk.TOP
        )

        self.progress_bar.pack(
            padx=self.theme.padding, pady=self.theme.padding, side=tk.BOTTOM, fill=tk.X
        )

        self.progress_frame.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.X
        )

    def pack_open_log_button(self) -> None:
        """Show the open log button."""
        self.open_log_button.pack(
            padx=self.theme.padding, pady=self.theme.padding, side=tk.RIGHT
        )

    def unpack_open_log_button(self) -> None:
        """Hide the open log button."""
        self.open_log_button.pack_forget()

    def set_progress_bar(
        self, progress_value: float, progress_percentage: int, color: str = Color.MAIN
    ) -> None:
        """Update the progress bar and percentage.

        Args:
            progress_value: Progress value between 0 and 1.
            progress_percentage: Progress percentage to display.
            color: Color of the percentage text.
        """
        # Ensure progress_value is in the range [0, 1]
        progress_value = max(0, min(1, progress_value))

        # Update progress bar
        self.progress_bar.set(progress_value)

        # Update percentage label
        self.progress_bar_percentage.configure(
            text=f"{progress_percentage}%", text_color=color
        )

        # Update the UI
        self.update()

    def _open_log(self) -> None:
        """Open the log file."""
        self.logger_instance.open_log_file()
