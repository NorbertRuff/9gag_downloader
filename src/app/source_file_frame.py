"""Responsible for the source file handling.

This class is responsible for the source file handling.
It contains the source file frame with the source file label the source file entry and the source file select mechanism.
"""

import tkinter

import customtkinter as ctk
from src.utils import Theme


class SourceFrame(ctk.CTkFrame):
    def __init__(self, *args, theme: Theme, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_frame = ctk.CTkFrame(self, border_width=theme.border_width, border_color=theme.border_color)
        self.source_file_entry = ctk.CTkEntry(self.source_frame, width=theme.element_width)

        self.source_file_entry.insert(0, "/home/ruff/projects/9gag_downloader/input/Your 9GAG data.html")

        ctk.CTkLabel(self.source_frame, text="Source File: ", font=("Arial", 12)).pack(padx=theme.padding,
                                                                                       pady=theme.padding,
                                                                                       side=tkinter.LEFT)
        source_file_select_button = ctk.CTkButton(self.source_frame, text="Select 9gag.html", width=20)
        source_file_select_button.pack(padx=theme.padding, pady=theme.padding, side=tkinter.RIGHT)
        source_file_select_button.bind("<Button-1>", lambda event: self.select_source_folder())
        self.source_file_entry.pack(padx=theme.padding, pady=theme.padding, side=tkinter.RIGHT)
        self.source_frame.pack(padx=theme.padding, pady=theme.padding, fill=tkinter.X)

    def get_entry_value(self) -> str:
        """ returns selected value as a string, returns an empty string if entry is empty """
        return self.source_file_entry.get()

    def set_entry_value(self, value: str) -> None:
        """ sets the value of source_file_entry """
        self.source_file_entry.insert(0, value)

    def select_source_folder(self) -> None:
        """ opens a file dialog to select a file """
        self.source_file_entry.delete(0, tkinter.END)
        self.source_file_entry.insert(0, tkinter.filedialog.askopenfilename())
