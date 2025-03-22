"""Download frame containing the download button and status message.

This frame contains the download button and a status message to inform the user
about the current state of the download process.
"""

import tkinter as tk
from typing import Any, Callable, Dict

import customtkinter as ctk

from src.config import Color, Theme


class DownloadFrame(ctk.CTkFrame):
    """Frame containing the download button and status message."""

    def __init__(
        self,
        master: Any,
        theme: Theme,
        start_download_callback: Callable[[], None],
        **kwargs: Dict[str, Any],
    ):
        """Initialize the download frame.

        Args:
            master: Parent widget.
            theme: Theme configuration.
            start_download_callback: Function to call when the download button is clicked.
            **kwargs: Additional keyword arguments to pass to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.theme = theme
        self.start_download_callback = start_download_callback
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and place the widgets in the frame."""
        # Create download frame
        self.download_frame = ctk.CTkFrame(
            self,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
        )

        # Create progress message
        self.progress_message = ctk.CTkLabel(
            self.download_frame, text="", font=("Arial", 16), wraplength=600
        )

        # Create download button
        self.download_button = ctk.CTkButton(
            self.download_frame,
            text="Download",
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            text_color=self.theme.button_text_color,
            command=self._on_download_click,
        )

        # Pack widgets
        self.progress_message.pack(padx=self.theme.padding, pady=self.theme.padding)

        self.download_button.pack(padx=self.theme.padding, pady=self.theme.padding)

        self.download_frame.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.X
        )

    def _on_download_click(self) -> None:
        """Handle the download button click event."""
        # Disable the download button before starting the download
        self.disable_download_button()
        # Start the download
        self.start_download_callback()

    def disable_download_button(self) -> None:
        """Disable the download button."""
        self.download_button.configure(state=tk.DISABLED)

    def enable_download_button(self) -> None:
        """Enable the download button."""
        self.download_button.configure(state=tk.NORMAL)

    def set_progress_message(self, text: str, color: str = Color.WHITE) -> None:
        """Set the status message.

        Args:
            text: Message text to display.
            color: Text color.
        """
        self.progress_message.configure(text=text, text_color=color)
