"""HTML parser using BeautifulSoup to extract gag information."""

from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

from src.core.models import Gag


class HtmlParser:
    """Parser for 9GAG HTML data exports."""

    @staticmethod
    def read_html_file(file_path: str) -> BeautifulSoup:
        """Read an HTML file and return a BeautifulSoup object.

        Args:
            file_path: Path to the HTML file.

        Returns:
            BeautifulSoup object.
        """
        with open(file_path, "r", encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        return soup

    @classmethod
    def get_gags_from_table(cls, table: BeautifulSoup) -> List[Gag]:
        """Extract gag details from a table element.

        Args:
            table: BeautifulSoup table element.

        Returns:
            List of Gag objects.
        """
        gags = []
        for tr in table.find_all("tr"):
            columns = tr.find_all("td")
            if columns and len(columns) > 2:
                # Extract id from URL
                href = (
                    columns[1].a["href"]
                    if columns[1].a and columns[1].a.has_attr("href")
                    else ""
                )
                gag_id = href.split("/")[-1] if href else ""

                # Extract title
                title = columns[2].text.strip() if columns[2].text else "No Title"

                if gag_id:
                    gags.append(Gag(id=gag_id, title=title))

        return gags

    @classmethod
    def extract_gags(
        cls, soup: BeautifulSoup, upvoted_gags: bool = False, saved_gags: bool = False
    ) -> List[Gag]:
        """Extract gags from BeautifulSoup object.

        Args:
            soup: BeautifulSoup object.
            upvoted_gags: Whether to extract upvoted gags.
            saved_gags: Whether to extract saved gags.

        Returns:
            List of Gag objects.
        """
        gags = []

        if upvoted_gags:
            upvotes_headers = soup.find_all("h3", text="Upvotes")
            if upvotes_headers and len(upvotes_headers) > 0:
                up_votes_table = upvotes_headers[0].find_next("table")
                if up_votes_table:
                    gags.extend(cls.get_gags_from_table(up_votes_table))

        if saved_gags:
            saved_headers = soup.find_all("h3", text="Saved")
            if saved_headers and len(saved_headers) > 0:
                saved_table = saved_headers[0].find_next("table")
                if saved_table:
                    gags.extend(cls.get_gags_from_table(saved_table))

        return gags

    @classmethod
    def parse_file(
        cls, file_path: str, upvoted_gags: bool = False, saved_gags: bool = False
    ) -> List[Gag]:
        """Parse a 9GAG HTML file and extract gags.

        Args:
            file_path: Path to the HTML file.
            upvoted_gags: Whether to extract upvoted gags.
            saved_gags: Whether to extract saved gags.

        Returns:
            List of Gag objects.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        soup = cls.read_html_file(str(file_path))
        return cls.extract_gags(soup, upvoted_gags, saved_gags)
