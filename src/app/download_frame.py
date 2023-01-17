""" Contains the DownloadFrame class.

This class is responsible for progress_message and the download button.

uses callback to communicate with the download loop.
"""

import tkinter

import customtkinter as ctk
from src.utils import Color, Theme


class DownloadFrame(ctk.CTkFrame):
    def __init__(self, *args, theme: Theme, start_download_callback, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_frame = ctk.CTkFrame(self, border_width=theme.border_width,
                                           border_color=theme.border_color)
        self.progress_message = ctk.CTkLabel(self.download_frame, text="", font=("Arial", 16))
        self.download_button = ctk.CTkButton(self.download_frame, text="Download", width=150, height=50,
                                             command=start_download_callback)

        self.progress_message.pack(padx=theme.padding, pady=theme.padding)
        self.download_button.pack(padx=theme.padding, pady=theme.padding)
        self.download_frame.pack(padx=theme.padding, pady=theme.padding, fill=tkinter.X)

    def disable_download_button(self) -> None:
        """ disables the download button """
        self.download_button.configure(state=tkinter.DISABLED)

    def enable_download_button(self) -> None:
        """ enables the download button """
        self.download_button.configure(state=tkinter.NORMAL)

    def set_progress_message(self, text: str, color: Color = Color.WHITE) -> None:
        """ sets the progress message """
        self.progress_message.configure(text=text, text_color=color)
