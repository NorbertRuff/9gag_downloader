import os
import re
import tkinter
from time import sleep

import customtkinter
import requests

# System Settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("blue")

# Constants
BASE_URL = "https://9gag.com/photo/"
VIDEO_SUFFIX = "_460sv.mp4"
IMAGE_SUFFIX = "_700b.jpg"
IMAGE_SAVE_LOCATION = "gags/images"
VIDEO_SAVE_LOCATION = "gags/videos"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# App frame
app = customtkinter.CTk()
description_frame = customtkinter.CTkFrame(app)
source_frame = customtkinter.CTkFrame(app, border_width=2, border_color="blue")
destination_frame = customtkinter.CTkFrame(app, border_width=2, border_color="blue")
progress_frame = customtkinter.CTkFrame(app, border_width=2, border_color="blue")
description_frame.pack(padx=10, pady=10)
source_frame.pack(padx=10, pady=10)
destination_frame.pack(padx=10, pady=10)
progress_frame.pack(padx=10, pady=10, fill=tkinter.X)

source_file_entry = customtkinter.CTkEntry(source_frame, width=700)
destination_folder_entry = customtkinter.CTkEntry(destination_frame, width=700)
progress_bar_ui_element = customtkinter.CTkProgressBar(progress_frame, progress_color="#42f5b9", height=20, width=700)
progress_bar_percentage = customtkinter.CTkLabel(progress_frame, text="", font=("Arial", 20))
progress_message_ui_element = customtkinter.CTkLabel(progress_frame, text="", font=("Arial", 16))


def read_html_file(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        text = f.read()
        return text


def get_up_voted_ids(text):
    up_voted_line_start = text.find("<h3>Upvotes</h3>")
    up_voted_line_stop = text.find("<h3>Downvotes</h3>")
    up_voted_html_table = text[up_voted_line_start:up_voted_line_stop]
    up_voted_links = re.findall(r'href="(.+?)"', up_voted_html_table)
    up_voted_ids = [link.split("/")[-1] for link in up_voted_links]
    return up_voted_ids


def try_video_download(gag_id):
    video_url = f"{BASE_URL}{gag_id}{VIDEO_SUFFIX}"
    response = requests.get(video_url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Video Downloaded as {gag_id}.mp4")
        with open(f"{destination_folder_entry.get()}/{VIDEO_SAVE_LOCATION}/{gag_id}.mp4", "wb") as f:
            f.write(response.content)
        return True
    return False


def try_image_download(gag_id):
    image_url = f"{BASE_URL}{gag_id}{IMAGE_SUFFIX}"
    response = requests.get(image_url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Image Downloaded as {gag_id}.jpg")
        with open(f"{destination_folder_entry.get()}/{IMAGE_SAVE_LOCATION}/{gag_id}.jpg", "wb") as f:
            f.write(response.content)
        return True
    return False


def download_gag(gag_id):
    result = try_video_download(gag_id)
    if result:
        return
    result = try_image_download(gag_id)
    if result:
        return
    print("Failed to download gag with id: ", gag_id)


def create_dirs_if_not_exist(selected_path):
    if not selected_path:
        return
    if not os.path.exists(selected_path + "/gags"):
        os.mkdir(selected_path + "/gags")
    if not os.path.exists(selected_path + "/gags/images"):
        os.mkdir(selected_path + "/gags/images")
    if not os.path.exists(selected_path + "/gags/videos"):
        os.mkdir(selected_path + "/gags/videos")


def setup_customtkinter():
    app.geometry("1024x768")
    app.title("9GAG Downloader")


def select_destination_folder(folder_path):
    folder_path.delete(0, tkinter.END)
    folder_path.insert(0, tkinter.filedialog.askdirectory())


def select_source_folder(folder_path):
    folder_path.delete(0, tkinter.END)
    folder_path.insert(0, tkinter.filedialog.askopenfilename())


def start_download_progress(path):
    up_voted_ids = read_9gag_data()
    if not up_voted_ids:
        return
    create_dirs_if_not_exist(path)
    reset_progress_ui_elements()

    one_percent = len(up_voted_ids) / 100
    for i in range(len(up_voted_ids)):
        progress_bar_ui_element.set(i / one_percent / 100)
        progress_bar_percentage.configure(text=f"{int(i / one_percent)}%")
        sleep(0.01)
        app.update()
    progress_bar_percentage.configure(text="100%")
    progress_message_ui_element.configure(text="Finished")


def reset_progress_ui_elements():
    progress_message_ui_element.configure(text="Downloading...")
    progress_bar_ui_element.set(0)
    progress_bar_percentage.configure(text="0%")
    app.update()


def add_ui_elements():
    title = customtkinter.CTkLabel(description_frame, text="9GAG Downloader", font=("Arial", 20))
    sub_title = customtkinter.CTkLabel(description_frame, text="""
    This app will download all the gags you upvoted on 9GAG.
    
    Request your 9GAG data from https://9gag.com/settings/privacy
    You will receive an email with a link to download your data in a html file.
    
    Select the folder where you want to save the gags and click on the Download button.
    This will create a folder named 'gags' in the selected folder and save the gags in it.
    """, font=("Arial", 12))
    title.pack(padx=10, pady=10)
    sub_title.pack(padx=10, pady=10)

    source_location_label = customtkinter.CTkLabel(source_frame, text="Source File: ", font=("Arial", 12))
    source_location_label.pack(padx=10, pady=10, side=tkinter.LEFT)
    source_file_entry.pack(padx=10, pady=10, side=tkinter.LEFT)
    source_file_select_button = customtkinter.CTkButton(source_frame, text="Select 9gag.html", width=20)
    source_file_select_button.pack(padx=10, pady=10, side=tkinter.RIGHT)
    source_file_select_button.bind("<Button-1>", lambda event: select_source_folder(source_file_entry))

    save_location_label = customtkinter.CTkLabel(destination_frame, text="Destination Folder: ", font=("Arial", 12))
    save_location_label.pack(padx=10, pady=10, side=tkinter.LEFT)
    file_select_button = customtkinter.CTkButton(destination_frame, text="Select Folder", width=20)
    file_select_button.pack(padx=10, pady=10, side=tkinter.RIGHT)
    file_select_button.bind("<Button-1>", lambda event: select_destination_folder(destination_folder_entry))
    destination_folder_entry.pack(padx=10, pady=10)

    progress_bar_ui_element.pack(padx=10, pady=10)
    progress_bar_ui_element.set(0)
    progress_bar_percentage.pack(padx=10, pady=10)
    progress_message_ui_element.pack(padx=10, pady=10)
    download_button = customtkinter.CTkButton(progress_frame, text="Download", width=50, height=10,
                                              command=lambda: start_download_progress(
                                                  destination_folder_entry.get()))
    download_button.pack(padx=10, pady=10)


def main():
    setup_customtkinter()
    add_ui_elements()
    app.mainloop()


def read_9gag_data():
    up_voted_ids = None
    print("source_file_entry.get(): ", source_file_entry.get())
    if source_file_entry.get() == "":
        progress_message_ui_element.configure(text="Please select a source file", text_color="red")
        return None
    try:
        raw_text = read_html_file(source_file_entry.get())
        up_voted_ids = get_up_voted_ids(raw_text)
    except FileNotFoundError:
        print("9GAG data file not found")
        progress_message_ui_element.configure(text="9GAG data file not found", text_color="red")
    if not up_voted_ids:
        print("No upvoted gags found")
        progress_message_ui_element.configure(text="No upvoted gags found in the file", text_color="red")
    return up_voted_ids


if __name__ == '__main__':
    main()
