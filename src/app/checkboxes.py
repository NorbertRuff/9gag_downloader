""" Class for the checkboxes frame.

This class is responsible for the checkboxes frame.
It contains the options label and a frame with checkboxes.
"""
import tkinter

import customtkinter as ctk
from src.utils import Theme


class Checkboxes(ctk.CTkFrame):
    def __init__(self, *args, theme: Theme, **kwargs):
        super().__init__(*args, **kwargs)
        self.saved_gags_var = tkinter.BooleanVar()
        self.upvoted_gags_var = tkinter.BooleanVar()
        self.checkboxes_frame = ctk.CTkFrame(self, border_width=theme.border_width, border_color=theme.border_color)
        ctk.CTkLabel(self.checkboxes_frame, text="Options:").pack(padx=theme.padding, pady=theme.padding)
        saved_checkbox = ctk.CTkCheckBox(master=self, text="Saved Gags", variable=self.saved_gags_var)
        upvoted_checkbox = ctk.CTkCheckBox(master=self, text="Upvoted Gags", variable=self.upvoted_gags_var)
        self.checkboxes_frame.pack(padx=theme.padding, pady=theme.padding, fill=tkinter.X)
        saved_checkbox.pack(padx=theme.padding, pady=theme.padding)
        upvoted_checkbox.pack(padx=theme.padding, pady=theme.padding)

    def get_saved_gags_var(self):
        """ returns the value of saved_gags_var """
        return self.saved_gags_var.get()

    def get_upvoted_gags_var(self):
        """ returns the value of upvoted_gags_var """
        return self.upvoted_gags_var.get()
