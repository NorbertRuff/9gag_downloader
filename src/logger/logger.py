"""Logger setup and configuration."""


import logging


class Logger:
    def __init__(self, name, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.filename = name + ".log"
        self.format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.level = log_level
        self.file_mode = 'a'
        self.date_format = '%H:%M:%S'
        logging.basicConfig(filename=self.filename, level=self.level, format=self.format, filemode=self.file_mode, datefmt=self.date_format)

    def error(self, param):
        self.logger.error(param)

    def info(self, param):
        self.logger.info(param)

    def debug(self, param):
        self.logger.debug(param)

    def warning(self, param):
        self.logger.warning(param)
