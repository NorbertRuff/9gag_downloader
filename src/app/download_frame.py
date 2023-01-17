import tkinter

import customtkinter as ctk

from src.utils import Color


class DownloadFrame(ctk.CTkFrame):
    def __init__(self, *args, padding, border_width, border_color, start_download_callback, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_frame = ctk.CTkFrame(self, border_width=border_width,
                                           border_color=border_color)
        self.progress_message = ctk.CTkLabel(self.download_frame, text="", font=("Arial", 16))
        self.download_button = ctk.CTkButton(self.download_frame, text="Download", width=150, height=50,
                                             command=start_download_callback)

        self.progress_message.pack(padx=padding, pady=padding)
        self.download_button.pack(padx=padding, pady=padding)
        self.download_frame.pack(padx=padding, pady=padding, fill=tkinter.X)

    def disable_download_button(self):
        self.download_button.configure(state=tkinter.DISABLED)

    def enable_download_button(self):
        self.download_button.configure(state=tkinter.NORMAL)

    def set_progress_message(self, text, color=Color.WHITE):
        self.progress_message.configure(text=text, text_color=color)
