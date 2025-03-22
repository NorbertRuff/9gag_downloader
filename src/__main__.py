"""Main entry point for the application when run as a module."""

from src.app import App
from src.download_handler import DownloadHandler
from src.logger import Logger
from src.utils import Theme


def main():
    """Run the main application."""
    logger = Logger("9GAG Downloader")
    downloader = DownloadHandler(logger)
    theme = Theme()
    app = App(downloader=downloader, theme=theme, logger=logger)
    app.mainloop()


if __name__ == "__main__":
    main()
