"""Contains the ProgressBar class.

This class is responsible for the progress bar and the progress percentage.
"""

import tkinter

import customtkinter as ctk
from src.utils import Color, utils, Theme


class ProgressBar(ctk.CTkFrame):
    def __init__(self, *args, theme: Theme, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = theme.padding
        self.progress_frame = ctk.CTkFrame(self, border_width=theme.border_width, border_color=theme.border_color)
        ctk.CTkLabel(self.progress_frame, text="Progress:").pack(padx=theme.padding, pady=theme.padding,
                                                                 side=tkinter.LEFT)
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=Color.MAIN, height=20,
                                               width=theme.element_width)
        self.progress_bar_percentage = ctk.CTkLabel(self.progress_frame, text="", font=("Arial", 20))
        self.open_log_button = ctk.CTkButton(self.progress_frame, text="Open Log", width=150, height=50,
                                             command=utils.open_log)
        self.progress_bar.pack(padx=theme.padding, pady=theme.padding, side=tkinter.BOTTOM)
        self.progress_bar_percentage.pack(padx=theme.padding, pady=theme.padding, side=tkinter.TOP)
        self.progress_frame.pack(padx=theme.padding, pady=theme.padding, fill=tkinter.X)

    def pack_open_log_button(self) -> None:
        """ Reveals the open log button on main window """
        self.open_log_button.pack(padx=self.padding, pady=self.padding, side=tkinter.RIGHT)

    def unpack_open_log_button(self) -> None:
        """ Hides the open log button on main window """
        self.open_log_button.pack_forget()

    def set_progress_bar(self, progress_bar_value: float, progress_bar_percentage: int, color=Color.WHITE) -> None:
        """ sets the progress bar value and percentage """
        self.progress_bar.set(progress_bar_value)
        self.progress_bar_percentage.configure(text=f"{progress_bar_percentage}%", text_color=color)
        self.update()
