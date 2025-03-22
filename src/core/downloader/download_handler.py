"""DownloadHandler is responsible for downloading the gags.

It first checks if the gags are already downloaded.
It first tries as video and if it fails it will try as image.
"""

import re
from enum import Enum, auto
from pathlib import Path
from typing import Tuple

import requests
from src.core.models import Gag
from src.utils.logging import Logger


class ContentType(Enum):
    """Type of content to download."""

    VIDEO = auto()
    IMAGE = auto()


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
        """Initialize the download handler.

        Args:
            logger: Logger instance for logging messages.
        """
        self.destination_folder = ""
        self.logger = logger

    def _get_content_info(self, content_type: ContentType) -> Tuple[str, str, str]:
        """Get file extension, suffix, and save location based on content type.

        Args:
            content_type: Type of content (VIDEO or IMAGE).

        Returns:
            Tuple of (file_extension, url_suffix, save_location).
        """
        if content_type == ContentType.VIDEO:
            return ".mp4", self.VIDEO_SUFFIX, self.VIDEO_SAVE_LOCATION
        else:  # ContentType.IMAGE
            return ".jpg", self.IMAGE_SUFFIX, self.IMAGE_SAVE_LOCATION

    def _sanitize_title(self, title: str) -> str:
        """Sanitize a title for use in filenames.

        Args:
            title: Title to sanitize.

        Returns:
            Sanitized title.
        """
        sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
        return sanitized[:100]  # Limit length to 100 chars

    def _try_download(self, gag: Gag, content_type: ContentType) -> bool:
        """Try to download gag content of a specific type.

        Args:
            gag: Gag to download.
            content_type: Type of content to try downloading.

        Returns:
            True if download was successful, False otherwise.
        """
        # Get info based on content type
        file_ext, url_suffix, save_location = self._get_content_info(content_type)
        content_type_name = content_type.name.lower()

        # Sanitize title
        sanitized_title = self._sanitize_title(gag.title)

        # Create path
        file_path = (
            Path(self.destination_folder)
            / save_location
            / f"{sanitized_title}{file_ext}"
        )

        # Check if already downloaded
        if file_path.exists():
            self.logger.info(
                f"{content_type_name.capitalize()} already downloaded: {file_path.name}"
            )

            # Update gag with info
            gag.is_video = content_type == ContentType.VIDEO
            gag.url = str(file_path)
            return True

        # Download content
        content_url = f"{self.BASE_URL}{gag.id}{url_suffix}"
        try:
            response = requests.get(content_url, headers=self.HEADERS, timeout=10)

            if response.status_code == 200:
                self.logger.info(
                    f"{content_type_name.capitalize()} downloaded as {file_path.name}"
                )

                # Ensure directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Save content
                with open(file_path, "wb") as f:
                    f.write(response.content)

                # Update gag with info
                gag.is_video = content_type == ContentType.VIDEO
                gag.url = str(file_path)
                return True

        except requests.RequestException as e:
            self.logger.error(f"Error downloading {content_type_name}: {str(e)}")

        return False

    def try_video_download(self, gag: Gag) -> bool:
        """Try to download the gag as a video.

        Args:
            gag: Gag to download.

        Returns:
            True if video download was successful, False otherwise.
        """
        return self._try_download(gag, ContentType.VIDEO)

    def try_image_download(self, gag: Gag) -> bool:
        """Try to download the gag as an image.

        Args:
            gag: Gag to download.

        Returns:
            True if image download was successful, False otherwise.
        """
        return self._try_download(gag, ContentType.IMAGE)

    def download_gag(self, gag: Gag, destination_folder: str) -> bool:
        """Download a gag, trying first as video then as image.

        Args:
            gag: Gag to download.
            destination_folder: Folder to save the downloaded content.

        Returns:
            True if download was successful, False otherwise.
        """
        self.destination_folder = destination_folder

        # Ensure base directories exist
        Path(destination_folder).mkdir(parents=True, exist_ok=True)

        # Try downloading as video first
        if self.try_video_download(gag):
            return True

        # If video download fails, try as image
        if self.try_image_download(gag):
            return True

        # Both download attempts failed
        self.logger.error(f"Failed to download gag: {gag.full_url}")
        return False
