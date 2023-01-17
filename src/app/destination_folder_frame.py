"""Class for the destination folder frame.

This class is responsible for the destination folder frame.
It contains a label, an entry and a button.
"""
import tkinter

import customtkinter as ctk
from src.utils import Theme


class DestinationFrame(ctk.CTkFrame):
    def __init__(self, *args, theme: Theme, **kwargs):
        super().__init__(*args, **kwargs)
        self.destination_frame = ctk.CTkFrame(self, border_width=theme.border_width, border_color=theme.border_color)
        self.destination_folder_entry = ctk.CTkEntry(self.destination_frame, width=theme.element_width)
        self.destination_folder_entry.insert(0, "/home/ruff/projects/9gag_downloader/")

        ctk.CTkLabel(self.destination_frame, text="Destination Folder: ", font=("Arial", 12)).pack(padx=theme.padding,
                                                                                                   pady=theme.padding,
                                                                                                   side=tkinter.LEFT)
        destination_folder_select_button = ctk.CTkButton(self.destination_frame, text="Select Folder.html", width=20)
        destination_folder_select_button.pack(padx=theme.padding, pady=theme.padding, side=tkinter.RIGHT)
        destination_folder_select_button.bind("<Button-1>", lambda event: self.select_destination_folder())
        self.destination_frame.pack(padx=theme.padding, pady=theme.padding, fill=tkinter.X)
        self.destination_folder_entry.pack(padx=theme.padding, pady=theme.padding, side=tkinter.RIGHT)

    def get_entry_value(self):
        """ returns selected value as a string, returns an empty string if entry is empty """
        return self.destination_folder_entry.get()

    def set_entry_value(self, value):
        """ sets the value of destination_folder_entry """
        self.destination_folder_entry.insert(0, value)

    def select_destination_folder(self):
        """ opens a file dialog to select a folder """
        self.destination_folder_entry.delete(0, tkinter.END)
        self.destination_folder_entry.insert(0, tkinter.filedialog.askdirectory())
