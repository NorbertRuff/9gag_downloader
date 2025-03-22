"""Source file frame for selecting the 9GAG data file.

This frame allows the user to select the HTML file containing their 9GAG data.
"""

import tkinter as tk
from tkinter import filedialog
from typing import Any, Dict, Optional

import customtkinter as ctk

from src.config import Theme


class SourceFileFrame(ctk.CTkFrame):
    """Frame for selecting the source HTML file."""

    def __init__(self, master: Any, theme: Theme, **kwargs: Dict[str, Any]):
        """Initialize the source file frame.

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
        # Create source file frame
        source_frame = ctk.CTkFrame(
            self,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
        )

        # Create source file entry
        self.source_file_entry = ctk.CTkEntry(
            source_frame,
            width=self.theme.element_width,
            placeholder_text="Select your 9GAG data file",
            font=("Arial", 12),
        )

        # Create source file label
        ctk.CTkLabel(
            source_frame, text="Source File:", font=("Arial", 12, "bold")
        ).pack(padx=self.theme.padding, pady=self.theme.padding, side=tk.LEFT)

        # Create source file select button
        source_file_select_button = ctk.CTkButton(
            source_frame,
            text="Select 9gag.html",
            width=120,
            font=("Arial", 11),
            command=self.select_source_file,
        )

        # Pack widgets
        source_file_select_button.pack(
            padx=self.theme.padding, pady=self.theme.padding, side=tk.RIGHT
        )

        self.source_file_entry.pack(
            padx=self.theme.padding,
            pady=self.theme.padding,
            side=tk.RIGHT,
            fill=tk.X,
            expand=True,
        )

        source_frame.pack(padx=self.theme.padding, pady=self.theme.padding, fill=tk.X)

    def get_entry_value(self) -> str:
        """Get the selected file path.

        Returns:
            Selected file path as a string, or an empty string if no file is selected.
        """
        return self.source_file_entry.get()

    def set_entry_value(self, value: str) -> None:
        """Set the file path.

        Args:
            value: File path to set.
        """
        self.source_file_entry.delete(0, tk.END)
        self.source_file_entry.insert(0, value)

    def select_source_file(self) -> None:
        """Open a file dialog to select a file and update the entry."""
        file_path = filedialog.askopenfilename(
            title="Select 9GAG Data File",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
        )

        if file_path:
            self.set_entry_value(file_path)
