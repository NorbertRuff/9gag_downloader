"""Source file frame for selecting the 9GAG data file.

This frame allows the user to select the HTML file containing their 9GAG data.
"""

import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from typing import Any, Callable, Dict, List, Optional

import customtkinter as ctk

from src.config import Color, Theme


class SourceFileFrame(ctk.CTkFrame):
    """Frame for selecting the source HTML file."""

    def __init__(
        self,
        master: Any,
        theme: Theme,
        recent_files: Optional[List[str]] = None,
        **kwargs: Dict[str, Any],
    ):
        """Initialize the source file frame.

        Args:
            master: Parent widget.
            theme: Theme configuration.
            recent_files: List of recently used files.
            **kwargs: Additional keyword arguments to pass to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.theme = theme
        self.recent_files = recent_files or []

        # Initialize value tracking for file path
        self._file_path = ""

        # File changed callback
        self.file_changed_callback: Optional[Callable[[str], None]] = None

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
            container, text="Source File", font=self.theme.title_font, anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, self.theme.small_padding))

        # Create input row
        input_row = ctk.CTkFrame(container, fg_color="transparent")
        input_row.pack(fill=tk.X, pady=self.theme.small_padding)

        # Create source file entry with rounded corners
        self.source_file_entry = ctk.CTkEntry(
            input_row,
            width=self.theme.element_width,
            placeholder_text="Select your 9GAG data file",
            font=self.theme.normal_font,
            fg_color=self.theme.entry_bg,
            text_color=self.theme.entry_fg,
            placeholder_text_color=self.theme.entry_placeholder_color,
            corner_radius=self.theme.corner_radius,
        )

        # Create button container
        button_container = ctk.CTkFrame(input_row, fg_color="transparent")

        # Create source file select button
        self.select_button = ctk.CTkButton(
            button_container,
            text="Select File",
            width=self.theme.button_width,
            height=self.theme.button_height,
            font=self.theme.normal_font,
            fg_color=self.theme.button_color,
            hover_color=self.theme.button_hover_color,
            text_color=self.theme.button_text_color,
            corner_radius=self.theme.button_corner_radius,
            command=self.select_source_file,
        )

        # Create recent files button if we have recent files
        if self.recent_files:
            self.recent_button = ctk.CTkButton(
                button_container,
                text="Recent",
                width=self.theme.button_width // 2,
                height=self.theme.button_height,
                font=self.theme.normal_font,
                fg_color=self.theme.button_color,
                hover_color=self.theme.button_hover_color,
                text_color=self.theme.button_text_color,
                corner_radius=self.theme.button_corner_radius,
                command=self._show_recent_files,
            )
            self.recent_button.pack(side=tk.LEFT, padx=(0, self.theme.small_padding))

        # Pack select button
        self.select_button.pack(side=tk.LEFT)

        # Pack widgets from right to left
        button_container.pack(side=tk.RIGHT, padx=(self.theme.small_padding, 0))
        self.source_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add help text
        help_text = ctk.CTkLabel(
            container,
            text="Select the HTML file you received from 9GAG containing your data.",
            font=self.theme.small_font,
            text_color=self.theme.entry_placeholder_color,
            anchor="w",
        )
        help_text.pack(anchor="w", pady=(self.theme.small_padding, 0))

        # Create recent files dropdown menu (initially hidden)
        self.recent_menu = None

    def _show_recent_files(self) -> None:
        """Show a dropdown menu with recent files."""
        if not self.recent_files:
            return

        # Create a toplevel for the dropdown menu
        self.recent_menu = tk.Menu(self, tearoff=0)

        # Add recent files to the menu
        for file_path in self.recent_files:
            # Show only the file name in the menu, but store the full path
            file_name = os.path.basename(file_path)
            self.recent_menu.add_command(
                label=file_name,
                command=lambda path=file_path: self.set_entry_value(path),
            )

        # Position and show the menu below the recent button
        x = self.recent_button.winfo_rootx()
        y = self.recent_button.winfo_rooty() + self.recent_button.winfo_height()
        self.recent_menu.post(x, y)

    def set_file_changed_callback(self, callback: Callable[[str], None]) -> None:
        """Set the callback for when the file changes.

        Args:
            callback: Function to call when the file changes.
                     Takes one string argument: file_path.
        """
        self.file_changed_callback = callback

    def get_entry_value(self) -> str:
        """Get the selected file path.

        Returns:
            Selected file path as a string, or an empty string if no file is selected.
        """
        return self._file_path

    def set_entry_value(self, value: str) -> None:
        """Set the file path.

        Args:
            value: File path to set.
        """
        # Clear current value
        self.source_file_entry.delete(0, tk.END)

        # Update stored path and entry value
        self._file_path = value

        # Display the filename (truncated if too long)
        self.source_file_entry.insert(0, self._format_path(value))

        # Call callback if set
        if self.file_changed_callback:
            self.file_changed_callback(value)

    def _format_path(self, path: str) -> str:
        """Format the path for display in the entry field.

        For usability, only show the filename and parent directory.

        Args:
            path: Full path to format

        Returns:
            Formatted path string
        """
        if not path:
            return ""

        # Convert to Path object for easier manipulation
        path_obj = Path(path)

        # Get the filename and parent directory
        filename = path_obj.name

        # Return the formatted path
        return path

    def select_source_file(self) -> None:
        """Open a file dialog to select a file and update the entry."""
        file_path = filedialog.askopenfilename(
            title="Select 9GAG Data File",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialdir=self._get_initial_dir(),
        )

        if file_path:
            self.set_entry_value(file_path)

    def _get_initial_dir(self) -> str:
        """Get the initial directory for the file dialog.

        Returns:
            Initial directory path.
        """
        # If we have a current file, use its directory
        if self._file_path:
            return str(Path(self._file_path).parent)

        # If we have recent files, use the directory of the most recent one
        if self.recent_files:
            return str(Path(self.recent_files[0]).parent)

        # Otherwise use the user's home directory
        return str(Path.home())
