import os
import re


def read_html_file(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        text = f.read()
        return text


def create_dirs_if_not_exist(selected_path):
    if not selected_path:
        return
    if not os.path.exists(selected_path + "/gags"):
        os.mkdir(selected_path + "/gags")
    if not os.path.exists(selected_path + "/gags/images"):
        os.mkdir(selected_path + "/gags/images")
    if not os.path.exists(selected_path + "/gags/videos"):
        os.mkdir(selected_path + "/gags/videos")


def get_up_voted_ids(text):
    gag_ids = []
    saved_line_start = text.find("<h3>Saved</h3>")
    up_voted_line_start = text.find("<h3>Upvotes</h3>")
    up_voted_line_stop = text.find("<h3>Downvotes</h3>")
    if (saved_line_start == -1) and (up_voted_line_start == -1):
        return gag_ids
    if up_voted_line_start == -1:
        return gag_ids

    up_voted_html_table = text[up_voted_line_start:up_voted_line_stop]
    saved_html_table = text[saved_line_start:up_voted_line_start]

    saved_links = re.findall(r'href="(.+?)"', saved_html_table)
    saved_ids = [saved.split("/")[-1] for saved in saved_links]

    up_voted_links = re.findall(r'href="(.+?)"', up_voted_html_table)
    up_voted_ids = [up_voted.split("/")[-1] for up_voted in up_voted_links]

    gag_ids.extend(up_voted_ids)
    gag_ids.extend(saved_ids)

    return gag_ids


def open_log():
    print(os.getcwd())
    os.startfile("9GAG Downloader.log", 'open')
