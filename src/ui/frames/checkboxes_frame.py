"""Checkboxes frame for selecting download options.

This frame contains checkboxes for selecting which types of gags to download.
"""

import tkinter as tk
from typing import Any, Dict

import customtkinter as ctk

from src.config import Theme


class CheckboxesFrame(ctk.CTkFrame):
    """Frame with checkboxes for selecting download options."""

    def __init__(self, master: Any, theme: Theme, **kwargs: Dict[str, Any]):
        """Initialize the checkboxes frame.

        Args:
            master: Parent widget.
            theme: Theme configuration.
            **kwargs: Additional keyword arguments to pass to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.theme = theme

        # Initialize variables
        self.saved_gags_var = tk.BooleanVar()
        self.upvoted_gags_var = tk.BooleanVar(value=True)  # Default selection

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and place the widgets in the frame."""
        # Create options frame
        options_frame = ctk.CTkFrame(
            self,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
        )

        # Add title label
        ctk.CTkLabel(options_frame, text="Options:", font=("Arial", 14, "bold")).pack(
            padx=self.theme.padding, pady=self.theme.padding
        )

        # Create checkboxes
        saved_checkbox = ctk.CTkCheckBox(
            master=options_frame,
            text="Saved Gags",
            variable=self.saved_gags_var,
            font=("Arial", 12),
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            corner_radius=4,
            hover=True,
        )

        upvoted_checkbox = ctk.CTkCheckBox(
            master=options_frame,
            text="Upvoted Gags",
            variable=self.upvoted_gags_var,
            font=("Arial", 12),
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            corner_radius=4,
            hover=True,
        )

        # Pack the frame and checkboxes
        options_frame.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.BOTH, expand=True
        )

        saved_checkbox.pack(padx=self.theme.padding, pady=self.theme.padding)
        upvoted_checkbox.pack(padx=self.theme.padding, pady=self.theme.padding)

    def get_saved_gags_var(self) -> bool:
        """Get the value of the saved gags checkbox.

        Returns:
            True if the checkbox is checked, False otherwise.
        """
        return self.saved_gags_var.get()

    def get_upvoted_gags_var(self) -> bool:
        """Get the value of the upvoted gags checkbox.

        Returns:
            True if the checkbox is checked, False otherwise.
        """
        return self.upvoted_gags_var.get()
