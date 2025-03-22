"""Main entry point for the application when run as a module."""

from src.config import Theme
from src.core.downloader import DownloadHandler
from src.ui import App
from src.utils.logging import Logger


def main():
    """Run the main application."""
    # Initialize logger
    logger = Logger("9GAG Downloader")
    logger.info("Starting application")

    # Initialize components
    downloader = DownloadHandler(logger)
    theme = Theme()

    # Create and run the app
    app = App(downloader=downloader, theme=theme, logger=logger)
    app.mainloop()

    logger.info("Application closed")


if __name__ == "__main__":
    main()
