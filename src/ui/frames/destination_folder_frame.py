"""Destination folder frame for selecting where to save the downloaded gags.

This frame allows the user to select the folder where the downloaded gags will be saved.
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from typing import Any, Callable, Dict, Optional

import customtkinter as ctk

from src.config import Theme


class DestinationFolderFrame(ctk.CTkFrame):
    """Frame for selecting the destination folder."""

    def __init__(self, master: Any, theme: Theme, **kwargs: Dict[str, Any]):
        """Initialize the destination folder frame.

        Args:
            master: Parent widget.
            theme: Theme configuration.
            **kwargs: Additional keyword arguments to pass to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.theme = theme

        # Initialize value tracking for folder path
        self._folder_path = ""

        # Folder changed callback
        self.folder_changed_callback: Optional[Callable[[str], None]] = None

        # Create UI elements
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and place the widgets in the frame."""
        # Create container frame with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.BOTH, expand=True
        )

        # Create title label
        title_label = ctk.CTkLabel(
            container, text="Destination Folder", font=self.theme.title_font, anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, self.theme.small_padding))

        # Create input row
        input_row = ctk.CTkFrame(container, fg_color="transparent")
        input_row.pack(fill=tk.X, pady=self.theme.small_padding)

        # Create destination folder entry with rounded corners
        self.destination_folder_entry = ctk.CTkEntry(
            input_row,
            width=self.theme.element_width,
            placeholder_text="Select destination folder",
            font=self.theme.normal_font,
            fg_color=self.theme.entry_bg,
            text_color=self.theme.entry_fg,
            placeholder_text_color=self.theme.entry_placeholder_color,
            corner_radius=self.theme.corner_radius,
        )

        # Create destination folder select button
        self.select_button = ctk.CTkButton(
            input_row,
            text="Select Folder",
            width=self.theme.button_width,
            height=self.theme.button_height,
            font=self.theme.normal_font,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            text_color=self.theme.button_text_color,
            corner_radius=self.theme.button_corner_radius,
            command=self.select_destination_folder,
        )

        # Pack widgets from right to left
        self.select_button.pack(side=tk.RIGHT, padx=(self.theme.small_padding, 0))
        self.destination_folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add help text
        help_text = ctk.CTkLabel(
            container,
            text="Select the folder where downloaded gags will be saved.",
            font=self.theme.small_font,
            text_color=self.theme.entry_placeholder_color,
            anchor="w",
        )
        help_text.pack(anchor="w", pady=(self.theme.small_padding, 0))

    def set_folder_changed_callback(self, callback: Callable[[str], None]) -> None:
        """Set the callback for when the folder changes.

        Args:
            callback: Function to call when the folder changes.
                     Takes one string argument: folder_path.
        """
        self.folder_changed_callback = callback

    def get_entry_value(self) -> str:
        """Get the selected folder path.

        Returns:
            Selected folder path as a string, or an empty string if no folder is selected.
        """
        return self._folder_path

    def set_entry_value(self, value: str) -> None:
        """Set the folder path.

        Args:
            value: Folder path to set.
        """
        # Clear current value
        self.destination_folder_entry.delete(0, tk.END)

        # Update stored path and entry value
        self._folder_path = value

        # Display the path (truncated if too long)
        self.destination_folder_entry.insert(0, value)

        # Call callback if set
        if self.folder_changed_callback:
            self.folder_changed_callback(value)

    def select_destination_folder(self) -> None:
        """Open a directory dialog to select a folder and update the entry."""
        folder_path = filedialog.askdirectory(
            title="Select Destination Folder", initialdir=self._get_initial_dir()
        )

        if folder_path:
            self.set_entry_value(folder_path)

    def _get_initial_dir(self) -> str:
        """Get the initial directory for the folder dialog.

        Returns:
            Initial directory path.
        """
        # If we have a current folder, use it
        if self._folder_path:
            return self._folder_path

        # Otherwise use the user's home directory
        return str(Path.home())
