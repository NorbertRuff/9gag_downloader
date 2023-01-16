import tkinter
from time import sleep

import customtkinter as ctk
from src import utils
from src.download_handler import Downloader
from src.logger import Logger
from src.utils import Color


class App(ctk.CTk):
    border_width = 1
    border_color = Color.MAIN
    padding = 10
    element_width = 700

    def __init__(self, downloader: Downloader, logger: Logger):
        super().__init__()
        self.saved_gags_var = tkinter.BooleanVar()
        self.upvoted_gags_var = tkinter.BooleanVar()
        self.downloader = downloader
        self.logger = logger
        self.setup_custom_tkinter()

        self.description_frame = ctk.CTkFrame(self)
        self.source_frame = ctk.CTkFrame(self, border_width=self.border_width, border_color=self.border_color)
        self.destination_frame = ctk.CTkFrame(self, border_width=self.border_width,
                                              border_color=self.border_color)
        self.progress_frame = ctk.CTkFrame(self, border_width=self.border_width,
                                           border_color=self.border_color)
        self.download_frame = ctk.CTkFrame(self, border_width=self.border_width,
                                           border_color=self.border_color)
        self.checkboxes_frame = ctk.CTkFrame(self, border_width=self.border_width, border_color=self.border_color)

        self.source_file_entry = ctk.CTkEntry(self.source_frame, width=self.element_width)
        self.destination_folder_entry = ctk.CTkEntry(self.destination_frame, width=self.element_width)

        self.source_file_entry.insert(0, "/home/ruff/projects/9gag_downloader/input/Your 9GAG data.html")
        self.destination_folder_entry.insert(0, "/home/ruff/projects/9gag_downloader/")

        self.progress_message = ctk.CTkLabel(self.download_frame, text="", font=("Arial", 16))
        self.download_button = ctk.CTkButton(self.download_frame, text="Download", width=150, height=50,
                                             command=self.start_download_progress)
        ctk.CTkLabel(self.progress_frame, text="Progress:").pack(padx=self.padding, pady=self.padding,
                                                                 side=tkinter.LEFT)
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=Color.MAIN,
                                               height=20, width=self.element_width)
        self.progress_bar_percentage = ctk.CTkLabel(self.progress_frame, text="", font=("Arial", 20))

        self.open_log_button = ctk.CTkButton(self.progress_frame, text="Open Log", width=50, height=10,
                                             command=utils.open_log)
        self.description_frame.pack(padx=self.padding, pady=self.padding, fill=tkinter.X)
        self.source_frame.pack(padx=self.padding, pady=self.padding, fill=tkinter.X)
        self.destination_frame.pack(padx=self.padding, pady=self.padding, fill=tkinter.X)
        ctk.CTkLabel(self.checkboxes_frame, text="Options:").pack(padx=self.padding, pady=self.padding,
                                                                  side=tkinter.LEFT)
        self.checkboxes_frame.pack(padx=self.padding, pady=self.padding, fill=tkinter.X)
        self.download_frame.pack(padx=self.padding, pady=self.padding, fill=tkinter.X)

        self.progress_bar.pack(padx=self.padding, pady=self.padding, side=tkinter.BOTTOM)
        self.progress_bar_percentage.pack(padx=self.padding, pady=self.padding, side=tkinter.TOP)
        self.update()

        saved_checkbox = ctk.CTkCheckBox(master=self.checkboxes_frame, text="Saved Gags", variable=self.saved_gags_var)
        upvoted_checkbox = ctk.CTkCheckBox(master=self.checkboxes_frame, text="Upvoted Gags",
                                           variable=self.upvoted_gags_var)
        saved_checkbox.pack(padx=self.padding, pady=self.padding)
        upvoted_checkbox.pack(padx=self.padding, pady=self.padding)

    def setup_custom_tkinter(self):
        self.title("9GAG Downloader")
        self.geometry("1024x768")
        ctk.set_appearance_mode("dark")

    def start_download_progress(self):
        source_file = self.get_source_file()
        destination_folder = self.get_destination_folder()
        if not source_file:
            self.set_progress_message("Please select a source file.", color=Color.RED)
            return
        if not destination_folder:
            self.set_progress_message("Please select a destination folder.", color=Color.RED)
            return
        if (not self.saved_gags_var.get()) and (not self.upvoted_gags_var.get()):
            self.set_progress_message("Please select at least one option.", color=Color.RED)
            return
        gag_ids = self.get_gag_ids()
        if not gag_ids:
            self.logger.error("No upvoted or saved gags found")
            self.set_progress_message(text="No upvoted or saved gags found", color=Color.RED)
            return
        self.progress_frame.forget()
        self.progress_frame.pack(padx=self.padding, pady=self.padding, fill=tkinter.X)
        utils.create_dirs_if_not_exist(destination_folder)
        one_percent = len(gag_ids) / 100
        for i in range(len(gag_ids)):
            self.set_progress_bar(i / one_percent / 100, int(i / one_percent), f"Downloading gag with id: {gag_ids[i]}",
                                  color=Color.MAIN)
            # sleep(0.05)
            self.update()
            self.downloader.download_gag(gag_ids[i], destination_folder)
        self.set_progress_bar(100, 100, "Download complete", color=Color.GREEN)
        self.set_download_button_state(tkinter.NORMAL)
        self.open_log_button.pack(padx=self.padding, pady=self.padding, side=tkinter.RIGHT)

    def get_gag_ids(self):
        found_gag_ids = None
        try:
            raw_text = utils.read_html_file(self.get_source_file())
            found_gag_ids = utils.get_up_voted_ids(raw_text, self.upvoted_gags_var.get(), self.saved_gags_var.get())
        except FileNotFoundError:
            self.logger.error("9GAG data file not found")
            self.set_progress_message(text="9GAG data file not found", color=Color.RED)
        return found_gag_ids

    def get_destination_folder(self):
        return self.destination_folder_entry.get()

    def get_source_file(self):
        return self.source_file_entry.get()

    def set_progress_message(self, text, color=Color.WHITE):
        self.progress_message.configure(text=text, text_color=color)
        self.update()

    def set_download_button_state(self, state):
        self.download_button.configure(state=state)

    def set_progress_bar(self, progress_bar_value, progress_bar_percentage, progress_bar_message, color=Color.WHITE):
        self.progress_bar.set(progress_bar_value)
        self.progress_bar_percentage.configure(text=f"{progress_bar_percentage}%", text_color=color)
        self.progress_message.configure(text=progress_bar_message, text_color=color)
        self.update()

    def init_ui(self):
        ctk.CTkLabel(self.description_frame, text="9GAG Downloader", font=("Arial", 20)).pack(
            padx=self.padding, pady=self.padding)
        ctk.CTkLabel(self.description_frame, text="""
        This app will download all the gags you upvoted or saved on 9GAG.
        
        Request your 9GAG data from https://9gag.com/settings/privacy
        You will receive an email with a link to download your data in a html file.
        
        Select the folder where you want to save the gags and click on the Download button.
        This will create a folder named 'gags' in the selected folder and save the gags in it.
        
        Note: This app will only download the gags you upvoted or saved. It will not download the gags you commented on.
        Note: This app will not download the gags which are posts or albums. It will only download the gags which are images or videos.
        """, font=("Arial", 14)).pack(padx=self.padding, pady=self.padding)

        ctk.CTkLabel(self.source_frame, text="Source File: ", font=("Arial", 12)).pack(padx=self.padding,
                                                                                       pady=self.padding,
                                                                                       side=tkinter.LEFT)
        ctk.CTkLabel(self.destination_frame, text="Destination Folder: ", font=("Arial", 12)).pack(
            padx=self.padding, pady=self.padding, side=tkinter.LEFT)

        source_file_select_button = ctk.CTkButton(self.source_frame, text="Select 9gag.html", width=20)
        source_file_select_button.pack(padx=self.padding, pady=self.padding, side=tkinter.RIGHT)
        source_file_select_button.bind("<Button-1>", lambda event: self.select_source_folder())

        file_select_button = ctk.CTkButton(self.destination_frame, text="Select Folder", width=20)
        file_select_button.pack(padx=self.padding, pady=self.padding, side=tkinter.RIGHT)
        file_select_button.bind("<Button-1>", lambda event: self.select_destination_folder())
        self.source_file_entry.pack(padx=self.padding, pady=self.padding, side=tkinter.RIGHT)
        self.destination_folder_entry.pack(padx=self.padding, pady=self.padding, side=tkinter.RIGHT)
        self.progress_message.pack(padx=self.padding, pady=self.padding)
        self.download_button.pack(padx=self.padding, pady=self.padding)
        self.update()

    def select_destination_folder(self):
        self.destination_folder_entry.delete(0, tkinter.END)
        self.destination_folder_entry.insert(0, tkinter.filedialog.askdirectory())

    def select_source_folder(self):
        self.source_file_entry.delete(0, tkinter.END)
        self.source_file_entry.insert(0, tkinter.filedialog.askopenfilename())
