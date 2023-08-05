""" Helper functions """

import os
from typing import TypeAlias

from bs4 import BeautifulSoup

GagDetails: TypeAlias = list[dict[str, str]]


def read_html_file(file_name: str) -> BeautifulSoup:
    """ reads the html file and returns as text """
    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        return soup


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


def get_gag_details(table: BeautifulSoup) -> GagDetails:
    """ returns a list of gag ids """
    gags: GagDetails = []
    for tr in table.find_all('tr'):
        columns = tr.find_all('td')
        if columns:
            gags.append({'id': columns[1].a['href'].split('/')[-1],
                'title': columns[2].text if columns[2].text else "No Title", })
    return gags


def extract_gags(soup: BeautifulSoup, upvoted_gags: bool, saved_gags: bool) -> GagDetails:
    """ returns the scraped gag details """
    gags: GagDetails = []
    if upvoted_gags:
        up_votes = soup.find_all("h3", text="Upvotes")[0].find_next("table")
        gags.extend(get_gag_details(up_votes))
    if saved_gags:
        saved = soup.find_all("h3", text="Saved")[0].find_next("table")
        gags.extend(get_gag_details(saved))
    return gags


def open_log() -> None:
    """ opens the log file """
    print(os.getcwd())
    os.startfile("9GAG Downloader.log", 'open')
