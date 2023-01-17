import tkinter

import customtkinter as ctk

from src.utils import Color, utils


class ProgressBar(ctk.CTkFrame):
    def __init__(self, *args, padding, border_width, border_color, width, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = padding
        self.progress_frame = ctk.CTkFrame(self, border_width=border_width, border_color=border_color)
        ctk.CTkLabel(self.progress_frame, text="Progress:").pack(padx=padding, pady=padding, side=tkinter.LEFT)
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=Color.MAIN, height=20, width=width)
        self.progress_bar_percentage = ctk.CTkLabel(self.progress_frame, text="", font=("Arial", 20))
        self.open_log_button = ctk.CTkButton(self.progress_frame, text="Open Log", width=150, height=50,
                                             command=utils.open_log)
        self.progress_bar.pack(padx=padding, pady=padding, side=tkinter.BOTTOM)
        self.progress_bar_percentage.pack(padx=padding, pady=padding, side=tkinter.TOP)
        self.progress_frame.pack(padx=padding, pady=padding, fill=tkinter.X)

    def pack_open_log_button(self):
        self.open_log_button.pack(padx=self.padding, pady=self.padding, side=tkinter.RIGHT)

    def unpack_open_log_button(self):
        self.open_log_button.pack_forget()

    def set_progress_bar(self, progress_bar_value, progress_bar_percentage, color=Color.WHITE):
        self.progress_bar.set(progress_bar_value)
        self.progress_bar_percentage.configure(text=f"{progress_bar_percentage}%", text_color=color)
        self.update()
