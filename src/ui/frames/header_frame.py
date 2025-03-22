"""Header frame for the application.

This frame displays the application title and help button.
"""

import tkinter as tk
from typing import Any, Dict, Optional

import customtkinter as ctk

from src.config import Theme
from src.ui.components import HelpButton


class HeaderFrame(ctk.CTkFrame):
    """Header frame with application title and help button."""

    def __init__(self, master: Any, theme: Theme, **kwargs: Dict[str, Any]):
        """Initialize the header frame.

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
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.BOTH, expand=True
        )

        # Configure grid for title and help button
        header_container.grid_columnconfigure(0, weight=1)  # Title expands
        header_container.grid_columnconfigure(1, weight=0)  # Button fixed width

        # Add title label
        title_label = ctk.CTkLabel(
            header_container,
            text="9GAG Downloader",
            font=("Arial", 18, "bold"),
            anchor="w",
        )
        title_label.grid(
            row=0,
            column=0,
            padx=self.theme.padding,
            pady=self.theme.padding,
            sticky=tk.W,
        )

        # Add help button
        help_button = HelpButton(
            header_container,
            theme=self.theme,
            help_text=self._get_description_text(),
            title="About 9GAG Downloader",
            fg_color=self.theme.button_color,
            text_color=self.theme.button_text_color,
            text="Help",
            width=60,
            height=30,
        )
        help_button.grid(
            row=0,
            column=1,
            padx=self.theme.padding,
            pady=self.theme.padding,
            sticky=tk.E,
        )

    def _get_description_text(self) -> str:
        """Get the description text for the application.

        Returns:
            Description text.
        """
        return """This app will download all the gags you upvoted or saved on 9GAG.

Request your 9GAG data from https://9gag.com/settings/privacy
You will receive an email with a link to download your data as an HTML file.

Select the folder where you want to save the gags and click on the Download button.
This will create a folder named 'gags' in the selected folder and save the gags in it.

Note: This app will only download the gags you upvoted or saved.
Note: This app will not download posts or albums, only images and videos."""
