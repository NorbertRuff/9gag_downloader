"""Helper functions for the application."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from bs4 import BeautifulSoup


@dataclass
class GagDetail:
    """Data class representing a gag detail extracted from HTML."""

    id: str
    title: str
    url: Optional[str] = None


def read_html_file(file_name: str) -> BeautifulSoup:
    """Read an HTML file and returns a BeautifulSoup object.

    Args:
        file_name: Path to the HTML file.

    Returns:
        BeautifulSoup object.
    """
    with open(file_name, "r", encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup


def create_dirs_if_not_exist(selected_path: str) -> None:
    """Create gags folder structure if it does not exist.

    Args:
        selected_path: Base path where to create folders.
    """
    if not selected_path:
        return

    # Use Path for better cross-platform compatibility
    base_path = Path(selected_path)
    gags_path = base_path / "gags"
    images_path = gags_path / "images"
    videos_path = gags_path / "videos"

    # Create directories
    gags_path.mkdir(exist_ok=True)
    images_path.mkdir(exist_ok=True)
    videos_path.mkdir(exist_ok=True)


def get_gag_details(table: BeautifulSoup) -> List[GagDetail]:
    """Extract a list of gag details from a table.

    Args:
        table: BeautifulSoup table element containing gag data.

    Returns:
        List of GagDetail objects.
    """
    gags: List[GagDetail] = []
    for tr in table.find_all("tr"):
        columns = tr.find_all("td")
        if columns and len(columns) > 1:
            # Get href attribute safely
            href = (
                columns[1].a["href"]
                if columns[1].a and "href" in columns[1].a.attrs
                else ""
            )
            gag_id = href.split("/")[-1] if href else ""

            # Get title safely
            title = columns[2].text.strip() if columns[2].text else "No Title"

            if gag_id:
                gags.append(GagDetail(id=gag_id, title=title))
    return gags


def extract_gags(
    soup: BeautifulSoup, upvoted_gags: bool, saved_gags: bool
) -> List[GagDetail]:
    """Extract gag details from BeautifulSoup object.

    Args:
        soup: BeautifulSoup object of the HTML file.
        upvoted_gags: Whether to extract upvoted gags.
        saved_gags: Whether to extract saved gags.

    Returns:
        List of GagDetail objects.
    """
    gags: List[GagDetail] = []

    if upvoted_gags:
        upvotes_headers = soup.find_all("h3", text="Upvotes")
        if upvotes_headers and len(upvotes_headers) > 0:
            up_votes_table = upvotes_headers[0].find_next("table")
            if up_votes_table:
                gags.extend(get_gag_details(up_votes_table))

    if saved_gags:
        saved_headers = soup.find_all("h3", text="Saved")
        if saved_headers and len(saved_headers) > 0:
            saved_table = saved_headers[0].find_next("table")
            if saved_table:
                gags.extend(get_gag_details(saved_table))

    return gags


def open_log() -> None:
    """Open the log file with the system's default application."""
    log_path = Path.cwd() / "9GAG Downloader.log"

    print(f"Current working directory: {Path.cwd()}")

    if log_path.exists():
        os.startfile(str(log_path))
    else:
        print(f"Log file not found: {log_path}")
