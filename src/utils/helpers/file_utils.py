"""File utilities."""

import os
from pathlib import Path
from typing import Union


def ensure_dir_exists(directory_path: Union[str, Path]) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory.

    Returns:
        Pathlib Path object.
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_dirs_if_not_exist(selected_path: str) -> None:
    """Create gags folders if they don't exist.

    Args:
        selected_path: Base path to create folders in.
    """
    if not selected_path:
        return

    # Use pathlib for better cross-platform compatibility
    base_path = Path(selected_path)
    gags_path = base_path / "gags"
    images_path = gags_path / "images"
    videos_path = gags_path / "videos"

    # Create directories
    gags_path.mkdir(exist_ok=True)
    images_path.mkdir(exist_ok=True)
    videos_path.mkdir(exist_ok=True)
