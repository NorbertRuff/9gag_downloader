"""Logger setup and configuration."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 3,
) -> logging.Logger:
    """Set up and configure a logger.

    Args:
        name: Logger name.
        log_level: Logging level.
        log_file: Log file path. If None, no file handler will be added.
        console: Whether to log to console.
        max_file_size: Maximum log file size in bytes.
        backup_count: Number of backup log files to keep.

    Returns:
        Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_file_size, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


class Logger:
    """Wrapper around Python's logging module."""

    def __init__(
        self, name: str, log_level: int = logging.INFO, log_file: Optional[str] = None
    ):
        """Initialize a logger.

        Args:
            name: Logger name.
            log_level: Logging level.
            log_file: Log file path. If None, defaults to "{name}.log".
        """
        self.name = name
        self.log_file = log_file or f"{name}.log"
        self.logger = setup_logger(name, log_level, self.log_file)

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message: Message to log.
        """
        self.logger.error(message)

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message: Message to log.
        """
        self.logger.info(message)

    def debug(self, message: str) -> None:
        """Log a debug message.

        Args:
            message: Message to log.
        """
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """Log a warning message.

        Args:
            message: Message to log.
        """
        self.logger.warning(message)

    def open_log_file(self) -> None:
        """Open the log file with the system's default application."""
        if os.path.exists(self.log_file):
            if sys.platform == "win32":
                os.startfile(self.log_file)
            elif sys.platform == "darwin":  # macOS
                os.system(f'open "{self.log_file}"')
            elif "linux" in sys.platform:  # Linux
                os.system(f'xdg-open "{self.log_file}"')
        else:
            print(f"Log file not found: {self.log_file}")
