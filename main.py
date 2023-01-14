import os
import re
import tkinter
import customtkinter
from time import sleep

import requests

# System Settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("blue")

# Constants
BASE_URL = "https://9gag.com/photo/"
VIDEO_SUFFIX = "_460sv.mp4"
IMAGE_SUFFIX = "_700b.jpg"
SAVE_LOCATION = "./gags"
IMAGE_SAVE_LOCATION = "./gags/images"
VIDEO_SAVE_LOCATION = "./gags/videos"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# App frame
app = customtkinter.CTk()
folder_path = customtkinter.CTkEntry(app, width=700)
progress_message = customtkinter.CTkLabel(app, text="", font=("Arial", 20))
progress_bar = customtkinter.CTkProgressBar(app, progress_color="grey", height=20, width=700)
progress_bar_percentage = customtkinter.CTkLabel(app, text="", font=("Arial", 20))


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
        with open(f"{VIDEO_SAVE_LOCATION}/{gag_id}.mp4", "wb") as f:
            f.write(response.content)
        return True
    return False


def try_image_download(gag_id):
    image_url = f"{BASE_URL}{gag_id}{IMAGE_SUFFIX}"
    response = requests.get(image_url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Image Downloaded as {gag_id}.jpg")
        with open(f"{IMAGE_SAVE_LOCATION}/{gag_id}.jpg", "wb") as f:
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
    if not os.path.exists(selected_path+"/gags"):
        os.mkdir(selected_path+"/gags")
    if not os.path.exists(selected_path+"/gags/images"):
        os.mkdir(selected_path+"/gags/images")
    if not os.path.exists(selected_path+"/gags/videos"):
        os.mkdir(selected_path+"/gags/videos")


def setup_customtkinter():
    app.geometry("720x480")
    app.title("9GAG Downloader")


def select_folder(folder_path):
    folder_path.delete(0, tkinter.END)
    folder_path.insert(0, tkinter.filedialog.askdirectory())


def start_download_progress(path):
    up_voted_ids = read_9gag_data()
    create_dirs_if_not_exist(path)
    reset_progress_ui_elements()
    one_percent = len(up_voted_ids)/100
    for i in range(len(up_voted_ids)):
        progress_bar.set(i/one_percent/100)
        progress_bar_percentage.configure(text=f"{int(i/one_percent)}%")
        sleep(0.01)
        app.update()
    progress_message.configure(text="Finished")


def reset_progress_ui_elements():
    progress_message.configure(text="Downloading...")
    progress_bar.set(0)
    progress_bar_percentage.configure(text="0%")
    app.update()


def add_ui_elements():
    title = customtkinter.CTkLabel(app, text="9GAG Downloader", font=("Arial", 20))
    title.pack(padx=10, pady=10)
    sub_title = customtkinter.CTkLabel(app, text="Select a folder to save the upvoted gags\n"
                                                 "This will create a folder named 'gags' in the selected folder and save the gags in it\n"
                                                 "It will take a while depending on the number of gags you have upvoted")
    sub_title.pack(padx=10, pady=10)

    save_location_label = customtkinter.CTkLabel(app, text="Save Location")
    save_location_label.pack(pady=10)

    # folder_path.insert(0, "C:/Users/username/Downloads")
    folder_path.insert(0, "D:/Downloads (mozilla)")
    file_select_button = customtkinter.CTkButton(app, text="Select Folder", width=20)
    file_select_button.pack(pady=10)
    file_select_button.bind("<Button-1>", lambda event: select_folder(folder_path))

    folder_path.pack(padx=10, pady=10)

    download_button = customtkinter.CTkButton(app, text="Download", width=50, height=10, command=lambda: start_download_progress(folder_path.get()))
    download_button.pack(padx=10, pady=10)
    progress_bar.pack(padx=10, pady=10)
    progress_bar.set(0)
    progress_bar_percentage.pack(padx=10, pady=10)
    progress_message.pack(padx=10, pady=10)


def main():
    setup_customtkinter()
    add_ui_elements()
    app.mainloop()


def read_9gag_data():
    raw_text = None
    up_voted_ids = None
    try:
        raw_text = read_html_file("Your 9GAG data.html")
        up_voted_ids = get_up_voted_ids(raw_text)
    except FileNotFoundError:
        print("9GAG data file not found")
        progress_message.configure(text="9GAG data file not found", fg="red")
    return up_voted_ids


if __name__ == '__main__':
    main()
