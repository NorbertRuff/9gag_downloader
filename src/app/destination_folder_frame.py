import tkinter

import customtkinter as ctk


class DestinationFrame(ctk.CTkFrame):
    def __init__(self, *args, padding, border_width, border_color, width, **kwargs):
        super().__init__(*args, **kwargs)
        self.destination_frame = ctk.CTkFrame(self, border_width=border_width, border_color=border_color)
        self.destination_folder_entry = ctk.CTkEntry(self.destination_frame, width=width)
        self.destination_folder_entry.insert(0, "/home/ruff/projects/9gag_downloader/")

        ctk.CTkLabel(self.destination_frame, text="Destination Folder: ", font=("Arial", 12)).pack(padx=padding,
                                                                                       pady=padding,
                                                                                       side=tkinter.LEFT)
        destination_folder_select_button = ctk.CTkButton(self.destination_frame, text="Select Folder.html", width=20)
        destination_folder_select_button.pack(padx=padding, pady=padding, side=tkinter.RIGHT)
        destination_folder_select_button.bind("<Button-1>", lambda event: self.select_destination_folder())
        self.destination_frame.pack(padx=padding, pady=padding, fill=tkinter.X)
        self.destination_folder_entry.pack(padx=padding, pady=padding, side=tkinter.RIGHT)

    def get_entry_value(self):
        """ returns selected value as a string, returns an empty string if entry is empty """
        return self.destination_folder_entry.get()

    def set_entry_value(self, value):
        """ sets the value of destination_folder_entry """
        self.destination_folder_entry.insert(0, value)

    def select_destination_folder(self):
        self.destination_folder_entry.delete(0, tkinter.END)
        self.destination_folder_entry.insert(0, tkinter.filedialog.askdirectory())
