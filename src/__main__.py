"""Main entry point for the application when run as a module."""

from src.config import Theme, SettingsManager
from src.core.downloader import DownloadHandler
from src.ui import App
from src.utils.logging import Logger


def main():
    """Run the main application."""
    # Initialize logger
    logger = Logger("9GAG Downloader")
    logger.info("Starting application")

    # Initialize settings manager
    settings_manager = SettingsManager(logger)

    # Initialize components
    downloader = DownloadHandler(logger)
    theme = Theme()

    # Create and run the app
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
