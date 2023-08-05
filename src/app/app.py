""" Class for the main window.

This class is the frame for the main window.
It contains all the subframes and the main loop.
"""

import tkinter

import customtkinter as ctk
from src import utils
from src.app.checkboxes import Checkboxes
from src.app.destination_folder_frame import DestinationFrame
from src.app.download_frame import DownloadFrame
from src.app.header import Header
from src.app.progress_bar import ProgressBar
from src.app.source_file_frame import SourceFrame
from src.download_handler import DownloadHandler
from src.logger import Logger
from src.utils import Color, Theme


class App(ctk.CTk):
    def __init__(self, downloader: DownloadHandler, theme: Theme, logger: Logger):
        super().__init__()
        self.downloader = downloader
        self.theme = theme
        self.logger = logger
        self.setup_custom_tkinter()
        ctk.CTkLabel(self, text="9GAG Downloader", font=("Arial", 20)).grid(row=0, column=0, columnspan=2,
                                                                            sticky=tkinter.W + tkinter.E)
        self.header = Header(self, theme=self.theme)
        self.checkboxes_frame = Checkboxes(self, theme=self.theme)
        self.source_frame = SourceFrame(self, theme=self.theme)
        self.destination_frame = DestinationFrame(self, theme=self.theme)
        self.progress_frame = ProgressBar(self, theme=self.theme)
        self.download_frame = DownloadFrame(self, theme=self.theme,
                                            start_download_callback=self.start_download_progress)
        self.header.grid(row=1, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)
        self.checkboxes_frame.grid(row=1, column=1, columnspan=1, sticky=tkinter.W + tkinter.E)
        self.source_frame.grid(row=2, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        self.destination_frame.grid(row=3, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        self.download_frame.grid(row=4, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        self.update()

    def setup_custom_tkinter(self):
        """ Sets up the app to use customtkinter like themes and main grid."""
        self.title("9GAG Downloader")
        self.geometry(self.theme.geometry)
        ctk.set_appearance_mode(self.theme.appearance_mode)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def start_download_progress(self):
        """ Starts the download progress."""
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
        gags = self.scrape_gag_details(upvoted_gags_check, saved_gags_check)
        if not gags:
            self.logger.error("No upvoted or saved gags found")
            self.set_progress_message(text="No upvoted or saved gags found", color=Color.RED)
            return
        self.progress_frame.forget()
        self.progress_frame.grid(row=5, column=0, columnspan=2, sticky=tkinter.W + tkinter.E)
        utils.create_dirs_if_not_exist(destination_folder)
        one_percent = len(gags) / 100
        for i in range(len(gags)):
            self.progress_frame.set_progress_bar(i / one_percent / 100, int(i / one_percent), color=Color.MAIN)
            self.set_progress_message(f"Downloading gag with id: {gags[i]}", color=Color.GREEN)
            # sleep(0.05)
            self.update()
            self.downloader.download_gag(gags[i], destination_folder)
        self.progress_frame.set_progress_bar(100, 100, color=Color.GREEN)
        self.set_progress_message("Download finished", color=Color.GREEN)
        self.download_frame.enable_download_button()
        self.progress_frame.pack_open_log_button()
        self.update()

    def scrape_gag_details(self, upvoted_gags_check, saved_gags_check):
        """ Returns a list of gag ids from the source file."""
        found_gags = None
        try:
            soup = utils.read_html_file(self.source_frame.get_entry_value())
            found_gags = utils.extract_gags(soup, upvoted_gags=upvoted_gags_check, saved_gags=saved_gags_check)
        except FileNotFoundError:
            self.logger.error("9GAG data file not found")
            self.set_progress_message(text="9GAG data file not found", color=Color.RED)
        return found_gags

    def set_progress_message(self, text, color=Color.WHITE):
        """ Sets the main message to the given text and color."""
        self.download_frame.set_progress_message(text=text, color=color)
