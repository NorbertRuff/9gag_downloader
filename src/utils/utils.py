""" Helper functions """

import os
import re


def read_html_file(file_name: str) -> str:
    """ reads the html file and returns as text """
    with open(file_name, "r", encoding='utf-8') as f:
        text = f.read()
        return text


def create_dirs_if_not_exist(selected_path: str) -> None:
    """ creates the gags folder if it does not exist """
    if not selected_path:
        return
    if not os.path.exists(selected_path + "/gags"):
        os.mkdir(selected_path + "/gags")
    if not os.path.exists(selected_path + "/gags/images"):
        os.mkdir(selected_path + "/gags/images")
    if not os.path.exists(selected_path + "/gags/videos"):
        os.mkdir(selected_path + "/gags/videos")


def get_gag_ids(text: str, up_voted_line_start: int, up_voted_line_stop: int) -> list:
    """ returns a list of gag ids """
    gag_ids = []
    up_voted_html_table = text[up_voted_line_start:up_voted_line_stop]
    up_voted_links = re.findall(r'href="(.+?)"', up_voted_html_table)
    gag_ids.extend([up_voted.split("/")[-1] for up_voted in up_voted_links])
    return gag_ids


def get_up_voted_ids(text: str, upvoted_gags: bool, saved_gags: bool) -> list:
    """ returns a list of upvoted gag ids """
    gag_ids = []
    saved_line_start = text.find("<h3>Saved</h3>")
    up_voted_line_start = text.find("<h3>Upvotes</h3>")
    up_voted_line_stop = text.find("<h3>Downvotes</h3>")
    if upvoted_gags:
        gag_ids.extend(get_gag_ids(text, up_voted_line_start, up_voted_line_stop))
    if saved_gags:
        gag_ids.extend(get_gag_ids(text, saved_line_start, up_voted_line_start))
    return gag_ids


def open_log() -> None:
    """ opens the log file """
    print(os.getcwd())
    os.startfile("9GAG Downloader.log", 'open')
