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

    # Updated base URL
    BASE_URL = "https://img-9gag-fun.9cache.com/photo/"

    # Updated suffixes for different image and video formats
    # Video formats
    VIDEO_SUFFIX_460 = "_460sv.mp4"  # Small video
    VIDEO_SUFFIX_720 = "_720w_gt.mp4"  # HD video
    VIDEO_SUFFIX_WEBM = "_460svwm.webm"  # WebM format

    # Image formats
    IMAGE_SUFFIX_700 = "_700b.jpg"  # Standard image
    IMAGE_SUFFIX_460 = "_460s.jpg"  # Small image
    IMAGE_SUFFIX_WEBP = "_700bwp.webp"  # WebP format

    # Save locations
    IMAGE_SAVE_LOCATION = "gags/images"
    VIDEO_SAVE_LOCATION = "gags/videos"

    # Request headers
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://9gag.com/",
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
            return ".mp4", self.VIDEO_SUFFIX_720, self.VIDEO_SAVE_LOCATION
        else:  # ContentType.IMAGE
            return ".jpg", self.IMAGE_SUFFIX_700, self.IMAGE_SAVE_LOCATION

    def _try_download_with_suffix(
        self, gag: Gag, content_type: ContentType, suffix: str
    ) -> bool:
        """Try to download gag with a specific URL suffix.

        Args:
            gag: Gag to download.
            content_type: Type of content to try downloading.
            suffix: URL suffix to try.

        Returns:
            True if download was successful, False otherwise.
        """
        content_type_name = content_type.name.lower()
        file_ext = ".mp4" if content_type == ContentType.VIDEO else ".jpg"
        save_location = (
            self.VIDEO_SAVE_LOCATION
            if content_type == ContentType.VIDEO
            else self.IMAGE_SAVE_LOCATION
        )

        # Sanitize title
        sanitized_title = self._sanitize_title(gag.title)

        # Create path
        file_path = (
            Path(self.destination_folder)
            / save_location
            / f"{sanitized_title}{file_ext}"
        )

        self.logger.info(
            f"Attempting to download {content_type_name} for gag: {gag.id} - {gag.title}"
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
        content_url = f"{self.BASE_URL}{gag.id}{suffix}"
        self.logger.info(f"Requesting URL: {content_url}")

        try:
            response = requests.get(content_url, headers=self.HEADERS, timeout=10)

            self.logger.info(
                f"{content_type_name.capitalize()} download response code: {response.status_code}"
            )
            if response.status_code == 200:
                # Check content type header to confirm content type
                content_type_header = response.headers.get("Content-Type", "")
                self.logger.info(f"Content-Type header: {content_type_header}")

                # For videos, verify it's actually a video by checking content type
                if content_type == ContentType.VIDEO:
                    if (
                        "video" not in content_type_header.lower()
                        and "mp4" not in content_type_header.lower()
                    ):
                        if content_type_header == "text/html":
                            self.logger.warning(
                                f"Video URL responded with HTML, likely not a video: {content_url}"
                            )
                            return False
                        self.logger.warning(
                            f"Video URL responded with non-video content type: {content_type_header}"
                        )

                        # Check response size to make sure it's not an error page
                        content_length = len(response.content)
                        if (
                            content_length < 10000
                        ):  # Less than 10KB is probably not a valid video
                            return False

                # Check response size to make sure it's not an error page
                content_length = len(response.content)
                self.logger.info(f"Response content length: {content_length} bytes")

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
            else:
                self.logger.warning(
                    f"Failed to download {content_type_name}, response code: {response.status_code}"
                )

        except requests.RequestException as e:
            self.logger.error(f"Error downloading {content_type_name}: {str(e)}")

        return False

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
        if content_type == ContentType.VIDEO:
            # Try different video formats in order of preference
            if self._try_download_with_suffix(gag, content_type, self.VIDEO_SUFFIX_720):
                return True
            if self._try_download_with_suffix(gag, content_type, self.VIDEO_SUFFIX_460):
                return True
            return False
        else:  # ContentType.IMAGE
            # Try different image formats in order of preference
            if self._try_download_with_suffix(gag, content_type, self.IMAGE_SUFFIX_700):
                return True
            if self._try_download_with_suffix(gag, content_type, self.IMAGE_SUFFIX_460):
                return True
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
        self.logger.info(f"Trying video download first for gag ID: {gag.id}")
        if self.try_video_download(gag):
            self.logger.info(f"Successfully downloaded as video: {gag.id}")
            return True

        # If video download fails, try as image
        self.logger.info(
            f"Video download failed for gag ID: {gag.id}. Trying as image."
        )
        if self.try_image_download(gag):
            self.logger.info(f"Successfully downloaded as image: {gag.id}")
            return True

        # Both download attempts failed
        self.logger.error(f"Failed to download gag: {gag.full_url}")
        return False
