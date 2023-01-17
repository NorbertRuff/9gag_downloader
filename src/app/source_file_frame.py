import tkinter

import customtkinter as ctk


class SourceFrame(ctk.CTkFrame):
    def __init__(self, *args, padding, border_width, border_color, width, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_frame = ctk.CTkFrame(self, border_width=border_width, border_color=border_color)
        self.source_file_entry = ctk.CTkEntry(self.source_frame, width=width)

        self.source_file_entry.insert(0, "/home/ruff/projects/9gag_downloader/input/Your 9GAG data.html")

        ctk.CTkLabel(self.source_frame, text="Source File: ", font=("Arial", 12)).pack(padx=padding,
                                                                                       pady=padding,
                                                                                       side=tkinter.LEFT)
        source_file_select_button = ctk.CTkButton(self.source_frame, text="Select 9gag.html", width=20)
        source_file_select_button.pack(padx=padding, pady=padding, side=tkinter.RIGHT)
        source_file_select_button.bind("<Button-1>", lambda event: self.select_source_folder())
        self.source_file_entry.pack(padx=padding, pady=padding, side=tkinter.RIGHT)
        self.source_frame.pack(padx=padding, pady=padding, fill=tkinter.X)

    def get_entry_value(self):
        """ returns selected value as a string, returns an empty string if entry is empty """
        return self.source_file_entry.get()

    def set_entry_value(self, value):
        """ sets the value of source_file_entry """
        self.source_file_entry.insert(0, value)

    def select_source_folder(self):
        self.source_file_entry.delete(0, tkinter.END)
        self.source_file_entry.insert(0, tkinter.filedialog.askopenfilename())
