import tkinter
from time import sleep

import customtkinter as ctk

from src import utils
from src.app.checkboxes import Checkboxes
from src.app.destination_folder_frame import DestinationFrame
from src.app.download_frame import DownloadFrame
from src.app.header import Header
from src.app.progress_bar import ProgressBar
from src.app.source_file_frame import SourceFrame
from src.download_handler import Downloader
from src.logger import Logger
from src.utils import Color


class App(ctk.CTk):
    border_width = 1
    border_color = Color.MAIN
    padding = 10
    element_width = 1000

    def __init__(self, downloader: Downloader, logger: Logger):
        super().__init__()
        self.downloader = downloader
        self.logger = logger
        self.setup_custom_tkinter()
        ctk.CTkLabel(self, text="9GAG Downloader", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        self.header = Header(self, padding=self.padding)
        self.checkboxes_frame = Checkboxes(self, padding=self.padding, border_width=self.border_width, border_color=self.border_color)
        self.source_frame = SourceFrame(self, padding=self.padding, width=self.element_width,
                                        border_width=self.border_width, border_color=self.border_color)
        self.destination_frame = DestinationFrame(self, padding=self.padding, width=self.element_width,
                                                  border_width=self.border_width, border_color=self.border_color)
        self.progress_frame = ProgressBar(self, padding=self.padding, width=self.element_width,
                                          border_width=self.border_width, border_color=self.border_color)
        self.download_frame = DownloadFrame(self, padding=self.padding, border_width=self.border_width,
                                            border_color=self.border_color,
                                            start_download_callback=self.start_download_progress)
        self.header.grid(row=1, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)
        self.checkboxes_frame.grid(row=1, column=1, columnspan=1, sticky=tkinter.W + tkinter.E )
        self.source_frame.grid(row=2, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        self.destination_frame.grid(row=3, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        self.download_frame.grid(row=4, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        self.update()

    def setup_custom_tkinter(self):
        self.title("9GAG Downloader")
        self.geometry("1024x768")
        ctk.set_appearance_mode("dark")
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def start_download_progress(self):
        source_file = self.source_frame.get_entry_value()
        destination_folder = self.destination_frame.get_entry_value()
        saved_gags_check = self.checkboxes_frame.get_saved_gags_var()
        upvoted_gags_check = self.checkboxes_frame.get_upvoted_gags_var()
        if not source_file:
            self.set_progress_message("Please select a source file.", color=Color.RED)
            return
        if not destination_folder:
            self.set_progress_message("Please select a destination folder.", color=Color.RED)
            return
        if (not saved_gags_check) and (not upvoted_gags_check):
            self.set_progress_message("Please select at least one option.", color=Color.RED)
            return
        gag_ids = self.get_gag_ids(upvoted_gags_check, saved_gags_check)
        if not gag_ids:
            self.logger.error("No upvoted or saved gags found")
            self.set_progress_message(text="No upvoted or saved gags found", color=Color.RED)
            return
        self.progress_frame.forget()
        self.progress_frame.grid(row=5, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        utils.create_dirs_if_not_exist(destination_folder)
        one_percent = len(gag_ids) / 100
        for i in range(len(gag_ids)):
            self.progress_frame.set_progress_bar(i / one_percent / 100, int(i / one_percent), color=Color.MAIN)
            self.set_progress_message(f"Downloading gag with id: {gag_ids[i]}", color=Color.GREEN)
            # sleep(0.05)
            self.update()
            self.downloader.download_gag(gag_ids[i], destination_folder)
        self.progress_frame.set_progress_bar(100, 100, color=Color.GREEN)
        self.set_progress_message("Download finished", color=Color.GREEN)
        self.download_frame.enable_download_button()
        self.progress_frame.pack_open_log_button()
        self.update()

    def get_gag_ids(self, upvoted_gags_check, saved_gags_check):
        found_gag_ids = None
        try:
            raw_text = utils.read_html_file(self.source_frame.get_entry_value())
            found_gag_ids = utils.get_up_voted_ids(raw_text, upvoted_gags=upvoted_gags_check,
                                                   saved_gags=saved_gags_check)
        except FileNotFoundError:
            self.logger.error("9GAG data file not found")
            self.set_progress_message(text="9GAG data file not found", color=Color.RED)
        return found_gag_ids

    def set_progress_message(self, text, color=Color.WHITE):
        self.download_frame.set_progress_message(text=text, color=color)
