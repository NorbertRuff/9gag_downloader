"""DownloadHandler is responsible for downloading the gags.

It first checks if the gags are already downloaded.
It first tries as video and if it fails it will try as image.
"""
import os

import requests
from src.logger import Logger


class DownloadHandler:
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

    def try_video_download(self, gag_id: str) -> bool:
        """Tries to download the gag as video."""
        if os.path.exists(f"{self.destination_folder}/{self.VIDEO_SAVE_LOCATION}/{gag_id}.mp4"):
            self.logger.info(f"Video already downloaded: {gag_id}.mp4")
            return True
        video_url = f"{self.BASE_URL}{gag_id}{self.VIDEO_SUFFIX}"
        response = requests.get(video_url, headers=self.HEADERS)
        if response.status_code == 200:
            self.logger.info(f"Video Downloaded as {gag_id}.mp4")
            with open(f"{self.destination_folder}/{self.VIDEO_SAVE_LOCATION}/{gag_id}.mp4", "wb") as f:
                f.write(response.content)
            return True
        return False

    def try_image_download(self, gag_id: str) -> bool:
        """Tries to download the gag as image."""
        if os.path.exists(f"{self.destination_folder}/{self.IMAGE_SAVE_LOCATION}/{gag_id}.jpg"):
            self.logger.info(f"Image already downloaded: {gag_id}.jpg")
            return True
        image_url = f"{self.BASE_URL}{gag_id}{self.IMAGE_SUFFIX}"
        response = requests.get(image_url, headers=self.HEADERS)
        if response.status_code == 200:
            self.logger.info(f"Image Downloaded as {gag_id}.jpg")
            with open(f"{self.destination_folder}/{self.IMAGE_SAVE_LOCATION}/{gag_id}.jpg", "wb") as f:
                f.write(response.content)
            return True
        return False

    def download_gag(self, gag_id: str, destination_folder: str) -> None:
        """Download logic."""
        self.destination_folder = destination_folder
        result = self.try_video_download(gag_id)
        if result:
            return
        result = self.try_image_download(gag_id)
        if result:
            return
        self.logger.error(f"Failed to download gag: https://9gag.com/gag/{gag_id}")
