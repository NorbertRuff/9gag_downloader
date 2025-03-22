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
        # Create container frame with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.BOTH, expand=True
        )

        # Top section with label and percentage
        top_section = ctk.CTkFrame(container, fg_color="transparent")
        top_section.pack(fill=tk.X, pady=(0, self.theme.small_padding))

        # Create progress label
        progress_label = ctk.CTkLabel(
            top_section,
            text="Download Progress:",
            font=self.theme.normal_font,
            text_color=self.theme.text_color,
            anchor="w",
        )

        # Create percentage label
        self.progress_bar_percentage = ctk.CTkLabel(
            top_section,
            text="0%",
            font=self.theme.title_font,
            text_color=self.theme.text_color,
        )

        # Pack top section widgets
        progress_label.pack(side=tk.LEFT)
        self.progress_bar_percentage.pack(side=tk.RIGHT, padx=(10, 0))

        # Progress bar container for styling
        progress_container = ctk.CTkFrame(
            container,
            fg_color=self.theme.progress_background_color,
            corner_radius=self.theme.corner_radius,
            height=self.theme.progress_height,
        )
        progress_container.pack(fill=tk.X, pady=self.theme.small_padding)

        # Create progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_container,
            progress_color=self.theme.progress_color,
            height=self.theme.progress_height - 4,
            corner_radius=self.theme.corner_radius - 2,
            fg_color=self.theme.progress_background_color,
        )
        self.progress_bar.pack(fill=tk.X, expand=True, padx=2, pady=2)
        self.progress_bar.set(0)  # Initialize to 0

        # Create action buttons container
        button_container = ctk.CTkFrame(container, fg_color="transparent")
        button_container.pack(fill=tk.X, pady=(self.theme.padding, 0), anchor="e")

        # Create open log button (initially hidden)
        self.open_log_button = ctk.CTkButton(
            button_container,
            text="Open Log",
            width=self.theme.button_width,
            height=self.theme.button_height,
            font=self.theme.normal_font,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            text_color=self.theme.button_text_color,
            corner_radius=self.theme.button_corner_radius,
            command=self._open_log,
        )

        # Pack container from right
        button_container.pack(anchor="e")

    def pack_open_log_button(self) -> None:
        """Show the open log button."""
        self.open_log_button.pack(
            side=tk.RIGHT, padx=self.theme.small_padding, pady=self.theme.small_padding
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
