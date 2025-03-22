"""Destination folder frame for selecting where to save the downloaded gags.

This frame allows the user to select the folder where the downloaded gags will be saved.
"""

import tkinter as tk
from tkinter import filedialog
from typing import Any, Dict, Optional

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
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and place the widgets in the frame."""
        # Create destination frame
        destination_frame = ctk.CTkFrame(
            self,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
        )

        # Create destination folder entry
        self.destination_folder_entry = ctk.CTkEntry(
            destination_frame,
            width=self.theme.element_width,
            placeholder_text="Select destination folder",
            font=("Arial", 12),
        )

        # Create destination folder label
        ctk.CTkLabel(
            destination_frame, text="Destination Folder:", font=("Arial", 12, "bold")
        ).pack(padx=self.theme.padding, pady=self.theme.padding, side=tk.LEFT)

        # Create destination folder select button
        destination_folder_select_button = ctk.CTkButton(
            destination_frame,
            text="Select Folder",
            width=100,
            font=("Arial", 11),
            command=self.select_destination_folder,
        )

        # Pack widgets
        destination_folder_select_button.pack(
            padx=self.theme.padding, pady=self.theme.padding, side=tk.RIGHT
        )

        self.destination_folder_entry.pack(
            padx=self.theme.padding,
            pady=self.theme.padding,
            side=tk.RIGHT,
            fill=tk.X,
            expand=True,
        )

        destination_frame.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.X
        )

    def get_entry_value(self) -> str:
        """Get the selected folder path.

        Returns:
            Selected folder path as a string, or an empty string if no folder is selected.
        """
        return self.destination_folder_entry.get()

    def set_entry_value(self, value: str) -> None:
        """Set the folder path.

        Args:
            value: Folder path to set.
        """
        self.destination_folder_entry.delete(0, tk.END)
        self.destination_folder_entry.insert(0, value)

    def select_destination_folder(self) -> None:
        """Open a directory dialog to select a folder and update the entry."""
        folder_path = filedialog.askdirectory(title="Select Destination Folder")

        if folder_path:
            self.set_entry_value(folder_path)
