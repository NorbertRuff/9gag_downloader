"""Header frame for the application.

This frame displays the application description and instructions.
"""

import tkinter as tk
from typing import Any, Dict, Optional

import customtkinter as ctk

from src.config import Theme


class HeaderFrame(ctk.CTkFrame):
    """Header frame with application description and instructions."""

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
        description_frame = ctk.CTkFrame(self)
        description_frame.pack(
            padx=self.theme.padding, pady=self.theme.padding, fill=tk.X
        )

        ctk.CTkLabel(
            description_frame,
            text=self._get_description_text(),
            font=("Arial", 14),
            justify=tk.LEFT,
            wraplength=400,
        ).pack(padx=self.theme.padding, pady=self.theme.padding)

    def _get_description_text(self) -> str:
        """Get the description text for the application.

        Returns:
            Description text.
        """
        return """
This app will download all the gags you upvoted or saved on 9GAG.

Request your 9GAG data from https://9gag.com/settings/privacy
You will receive an email with a link to download your data as an HTML file.

Select the folder where you want to save the gags and click on the Download button.
This will create a folder named 'gags' in the selected folder and save the gags in it.

Note: This app will only download the gags you upvoted or saved.
Note: This app will not download posts or albums, only images and videos.
"""
