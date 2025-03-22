"""Utilities package for the application."""

from .utils import (
    GagDetail,
    create_dirs_if_not_exist,
    extract_gags,
    get_gag_details,
    open_log,
    read_html_file,
)

__all__ = [
    "GagDetail",
    "create_dirs_if_not_exist",
    "extract_gags",
    "get_gag_details",
    "open_log",
    "read_html_file",
]
