"""Download frame containing the download button and status message.

This frame contains the download button and a status message to inform the user
about the current state of the download process.
"""

import tkinter as tk
from typing import Any, Callable, Dict, Optional

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
        # Create main container frame
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.BOTH, expand=True
        )

        # Create status message container
        message_container = ctk.CTkFrame(container, fg_color="transparent")
        message_container.pack(fill=tk.X, pady=(0, self.theme.padding), expand=True)

        # Create status icon (initially hidden)
        self.status_icon = ctk.CTkLabel(
            message_container,
            text="",
            font=("Segoe UI", 18),
            width=30,
            text_color=Color.SUCCESS,
        )

        # Create progress message with background that matches the frame
        self.progress_message = ctk.CTkLabel(
            message_container,
            text="",
            font=self.theme.normal_font,
            wraplength=800,
            height=40,
            corner_radius=self.theme.corner_radius // 2,
            anchor="center",
            fg_color="transparent",
        )

        # Pack the message (icon will be shown when needed)
        self.progress_message.pack(fill=tk.X, expand=True)

        # Create button container for centering
        button_container = ctk.CTkFrame(container, fg_color="transparent")
        button_container.pack(fill=tk.X, pady=self.theme.padding)

        # Create download button with improved styling
        self.download_button = ctk.CTkButton(
            button_container,
            text="Download",
            width=self.theme.main_button_width,
            height=self.theme.main_button_height,
            font=self.theme.button_font,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            text_color=self.theme.button_text_color,
            corner_radius=self.theme.button_corner_radius,
            command=self._on_download_click,
            border_width=1,
            border_color=self.theme.button_hover_color,
        )

        # Center the button
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(2, weight=1)
        self.download_button.grid(
            row=0, column=1, padx=self.theme.padding, pady=self.theme.padding
        )

    def _show_status_icon(self, status: str) -> None:
        """Show the status icon based on the status type.

        Args:
            status: Status type ('success', 'error', 'warning')
        """
        # Set icon and color based on status
        if status == "success":
            self.status_icon.configure(text="✓", text_color=Color.SUCCESS)
        elif status == "error":
            self.status_icon.configure(text="✕", text_color=Color.ERROR)
        elif status == "warning":
            self.status_icon.configure(text="⚠", text_color=Color.WARNING)
        else:
            # Hide icon for neutral status
            self.status_icon.pack_forget()
            return

        # Show the icon
        self.status_icon.pack(side=tk.LEFT, padx=(0, 10))

    def _on_download_click(self) -> None:
        """Handle the download button click event."""
        # Clear any previous status message
        self.set_progress_message("")

        # Disable the download button before starting the download
        self.disable_download_button()

        # Start the download
        self.start_download_callback()

    def disable_download_button(self) -> None:
        """Disable the download button."""
        self.download_button.configure(
            state=tk.DISABLED,
            fg_color=self.theme.button_disabled_color,
            text="Downloading...",
        )

    def enable_download_button(self) -> None:
        """Enable the download button."""
        self.download_button.configure(
            state=tk.NORMAL, fg_color=self.theme.button_color, text="Download"
        )

    def set_progress_message(self, text: str, color: str = Color.WHITE) -> None:
        """Set the status message.

        Args:
            text: Message text to display.
            color: Text color.
        """
        self.progress_message.configure(text=text, text_color=color)

        # Show status icon based on color
        if color == Color.SUCCESS:
            self._show_status_icon("success")
        elif color == Color.ERROR:
            self._show_status_icon("error")
        elif color == Color.WARNING:
            self._show_status_icon("warning")
        else:
            self._show_status_icon("none")
