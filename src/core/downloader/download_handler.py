"""DownloadHandler is responsible for downloading the gags.

It first checks if the gags are already downloaded.
It first tries as video and if it fails it will try as image.
"""

import os
import re
from pathlib import Path

import requests
from src.core.models import Gag
from src.utils.logging import Logger


class DownloadHandler:
    """Handler for downloading 9GAG content."""

    BASE_URL = "https://9gag.com/photo/"
    VIDEO_SUFFIX = "_460sv.mp4"
    IMAGE_SUFFIX = "_700b.jpg"
    IMAGE_SAVE_LOCATION = "gags/images"
    VIDEO_SAVE_LOCATION = "gags/videos"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self, logger: Logger):
        self.destination_folder = ""
        self.logger = logger

    def try_video_download(self, gag: Gag) -> bool:
        """Tries to download the gag as video."""
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "", gag.title)
        sanitized_title = sanitized_title[:100]

        # Create path using pathlib for better cross-platform compatibility
        video_path = (
            Path(self.destination_folder)
            / self.VIDEO_SAVE_LOCATION
            / f"{sanitized_title}.mp4"
        )

        if video_path.exists():
            self.logger.info(f"Video already downloaded: {sanitized_title}.mp4")
            return True

        video_url = f"{self.BASE_URL}{gag.id}{self.VIDEO_SUFFIX}"
        response = requests.get(video_url, headers=self.HEADERS)

        if response.status_code == 200:
            self.logger.info(f"Video Downloaded as {sanitized_title}.mp4")

            # Ensure directory exists
            video_path.parent.mkdir(parents=True, exist_ok=True)

            with open(video_path, "wb") as f:
                f.write(response.content)

            # Update gag with info that it's a video
            gag.is_video = True
            gag.url = str(video_path)
            return True

        return False

    def try_image_download(self, gag: Gag) -> bool:
        """Tries to download the gag as image."""
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "", gag.title)
        sanitized_title = sanitized_title[:100]

        # Create path using pathlib for better cross-platform compatibility
        image_path = (
            Path(self.destination_folder)
            / self.IMAGE_SAVE_LOCATION
            / f"{sanitized_title}.jpg"
        )

        if image_path.exists():
            self.logger.info(f"Image already downloaded: {sanitized_title}.jpg")
            return True

        image_url = f"{self.BASE_URL}{gag.id}{self.IMAGE_SUFFIX}"
        response = requests.get(image_url, headers=self.HEADERS)

        if response.status_code == 200:
            self.logger.info(f"Image Downloaded as {sanitized_title}.jpg")

            # Ensure directory exists
            image_path.parent.mkdir(parents=True, exist_ok=True)

            with open(image_path, "wb") as f:
                f.write(response.content)

            # Update gag with info that it's an image
            gag.is_video = False
            gag.url = str(image_path)
            return True

        return False

    def download_gag(self, gag: Gag, destination_folder: str) -> None:
        """Download logic for a specific gag."""
        self.destination_folder = destination_folder

        # Ensure base directories exist
        Path(destination_folder).mkdir(parents=True, exist_ok=True)

        result = self.try_video_download(gag)
        if result:
            return

        result = self.try_image_download(gag)
        if result:
            return

        self.logger.error(f"Failed to download gag: {gag.full_url}")
