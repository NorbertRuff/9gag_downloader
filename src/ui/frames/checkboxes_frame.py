"""Checkboxes frame for selecting download options.

This frame contains checkboxes for selecting which types of gags to download.
"""

import tkinter as tk
from typing import Any, Callable, Dict, Optional

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

        # Callback for when checkboxes change
        self.checkbox_changed_callback: Optional[Callable[[bool, bool], None]] = None

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Create and place the widgets in the frame."""
        # Create options frame
        options_frame = ctk.CTkFrame(
            self,
            border_width=self.theme.border_width,
            border_color=self.theme.border_color,
        )

        title_label = ctk.CTkLabel(
            options_frame, text="Options:", font=self.theme.title_font, anchor="w"
        )

        title_label.pack(anchor="w", pady=(0, self.theme.small_padding))

        # Create checkboxes
        self.saved_checkbox = ctk.CTkCheckBox(
            master=options_frame,
            text="Saved Gags",
            variable=self.saved_gags_var,
            font=("Arial", 12),
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            corner_radius=4,
            hover=True,
            command=self._on_checkbox_change,
        )

        self.upvoted_checkbox = ctk.CTkCheckBox(
            master=options_frame,
            text="Upvoted Gags",
            variable=self.upvoted_gags_var,
            font=("Arial", 12),
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            corner_radius=4,
            hover=True,
            command=self._on_checkbox_change,
        )

        # Pack the frame
        options_frame.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.BOTH, expand=True
        )

        # Pack the checkboxes container
        options_frame.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.X, expand=True
        )

        # Pack checkboxes side by side
        self.saved_checkbox.pack(
            side=tk.LEFT, padx=self.theme.padding, pady=self.theme.padding
        )
        self.upvoted_checkbox.pack(
            side=tk.LEFT, padx=self.theme.padding, pady=self.theme.padding
        )

    def _bind_events(self) -> None:
        """Bind events for the checkboxes."""
        # The checkboxes already have commands, but we can add more bindings here if needed
        pass

    def _on_checkbox_change(self) -> None:
        """Handle checkbox state changes."""
        if self.checkbox_changed_callback:
            self.checkbox_changed_callback(
                self.saved_gags_var.get(), self.upvoted_gags_var.get()
            )

    def set_checkbox_changed_callback(
        self, callback: Callable[[bool, bool], None]
    ) -> None:
        """Set the callback for when checkbox states change.

        Args:
            callback: Function to call when checkbox states change.
                     Takes two boolean arguments: saved_selected and upvoted_selected.
        """
        self.checkbox_changed_callback = callback

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

    def set_saved_gags_var(self, value: bool) -> None:
        """Set the value of the saved gags checkbox.

        Args:
            value: Value to set (True for checked, False for unchecked).
        """
        if value:
            self.saved_checkbox.select()
        else:
            self.saved_checkbox.deselect()

    def set_upvoted_gags_var(self, value: bool) -> None:
        """Set the value of the upvoted gags checkbox.

        Args:
            value: Value to set (True for checked, False for unchecked).
        """
        if value:
            self.upvoted_checkbox.select()
        else:
            self.upvoted_checkbox.deselect()
