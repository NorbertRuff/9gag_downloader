"""Help button component.

This component provides a help button that displays a popup with information.
"""

import tkinter as tk
from typing import Any, Dict, Optional

import customtkinter as ctk

from src.config import Theme


class HelpButton(ctk.CTkButton):
    """Help button that shows information in a popup dialog."""

    def __init__(
        self,
        master: Any,
        theme: Theme,
        help_text: str,
        title: str = "Help",
        **kwargs: Dict[str, Any],
    ):
        """Initialize the help button.

        Args:
            master: Parent widget.
            theme: Theme configuration.
            help_text: Text to display in the help popup.
            title: Title for the help popup.
            **kwargs: Additional keyword arguments to pass to CTkButton.
        """
        self.theme = theme
        self.help_text = help_text
        self.title = title

        icon_path = kwargs.pop("icon", "ℹ️")
        text = kwargs.pop("text", "")
        width = kwargs.pop("width", 30)
        height = kwargs.pop("height", 30)
        corner_radius = kwargs.pop("corner_radius", 15)

        super().__init__(
            master,
            text=text,
            width=width,
            height=height,
            corner_radius=corner_radius,
            command=self._show_help_popup,
            **kwargs,
        )

        if not text:
            self.configure(text=icon_path)

    def _show_help_popup(self) -> None:
        """Show the help popup with the information text."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.title)
        dialog.geometry("600x400")
        dialog.resizable(True, True)
        dialog.grab_set()

        dialog.minsize(400, 300)

        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=0)

        text_container = ctk.CTkFrame(dialog)
        text_container.grid(row=0, column=0, padx=20, pady=20, sticky=tk.NSEW)
        text_container.grid_columnconfigure(0, weight=1)
        text_container.grid_rowconfigure(0, weight=1)

        text_widget = tk.Text(
            text_container,
            wrap=tk.WORD,
            bg=self._get_color_for_mode("#1A1A1A", "#F0F0F0"),
            fg=self._get_color_for_mode("#FFFFFF", "#000000"),
            padx=10,
            pady=10,
            font=("Arial", 12),
            borderwidth=0,
            highlightthickness=0,
        )
        text_widget.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ctk.CTkScrollbar(text_container, command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.insert(tk.END, self.help_text)
        text_widget.config(state=tk.DISABLED)

        close_button = ctk.CTkButton(dialog, text="Close", command=dialog.destroy)
        close_button.grid(row=1, column=0, padx=20, pady=20, sticky=tk.SE)

        dialog.update_idletasks()
        parent_x = self.winfo_toplevel().winfo_x()
        parent_y = self.winfo_toplevel().winfo_y()
        parent_width = self.winfo_toplevel().winfo_width()
        parent_height = self.winfo_toplevel().winfo_height()

        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        dialog.geometry(f"+{x}+{y}")

    def _get_color_for_mode(self, dark_color: str, light_color: str) -> str:
        """Get color based on appearance mode.

        Args:
            dark_color: Color to use in dark mode
            light_color: Color to use in light mode

        Returns:
            The appropriate color for the current mode
        """
        mode = ctk.get_appearance_mode().lower()
        return dark_color if mode == "dark" else light_color

    def set_help_text(self, text: str) -> None:
        """Update the help text.

        Args:
            text: New help text to display.
        """
        self.help_text = text
