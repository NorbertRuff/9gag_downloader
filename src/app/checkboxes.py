import tkinter

import customtkinter as ctk


class Checkboxes(ctk.CTkFrame):
    def __init__(self, *args, padding, border_width, border_color, **kwargs):
        super().__init__(*args, **kwargs)
        self.saved_gags_var = tkinter.BooleanVar()
        self.upvoted_gags_var = tkinter.BooleanVar()
        self.checkboxes_frame = ctk.CTkFrame(self, border_width=border_width, border_color=border_color)
        ctk.CTkLabel(self.checkboxes_frame, text="Options:").pack(padx=padding, pady=padding)
        saved_checkbox = ctk.CTkCheckBox(master=self, text="Saved Gags", variable=self.saved_gags_var)
        upvoted_checkbox = ctk.CTkCheckBox(master=self, text="Upvoted Gags", variable=self.upvoted_gags_var)
        self.checkboxes_frame.pack(padx=padding, pady=padding, fill=tkinter.X)
        saved_checkbox.pack(padx=padding, pady=padding)
        upvoted_checkbox.pack(padx=padding, pady=padding)

    def get_saved_gags_var(self):
        return self.saved_gags_var.get()

    def get_upvoted_gags_var(self):
        return self.upvoted_gags_var.get()
