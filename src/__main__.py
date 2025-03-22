"""Main entry point for the application."""

import sys
from pathlib import Path

from src.config import SettingsManager, Theme
from src.core.downloader import DownloadHandler
from src.core.models import Gag
from src.ui.app import App
from src.utils.logging import Logger


def test_download(logger):
    """Test download function to verify the download handler works correctly."""
    test_gag_id = "aW4nMjA"  # New 9GAG post ID from user (a video)
    test_gag = Gag(id=test_gag_id, title="Test Gag Video")

    logger.info("Starting download test")
    downloader = DownloadHandler(logger)

    # Create a test destination folder
    test_folder = Path("./test_downloads")
    test_folder.mkdir(exist_ok=True)

    logger.info(f"Testing download for gag ID: {test_gag_id}")
    result = downloader.download_gag(test_gag, str(test_folder))

    if result:
        logger.info(f"Download successful! Saved as {test_gag.url}")
        logger.info(f"Is video: {test_gag.is_video}")
    else:
        logger.error("Download failed!")

    return result


def main():
    """Start the application."""
    logger = Logger("9GAG Downloader")
    logger.info("Starting application")

    # Initialize components
    theme = Theme()
    settings_manager = SettingsManager()
    downloader = DownloadHandler(logger)

    # For debugging: Uncomment to test downloads directly
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_download(logger)
        return

    # Create and run app
    app = App(
        downloader=downloader,
        theme=theme,
        logger=logger,
        settings_manager=settings_manager,
    )
    app.mainloop()

    logger.info("Application closed")


if __name__ == "__main__":
    main()
