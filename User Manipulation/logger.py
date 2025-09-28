import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, app_logger, log_file="app.log", level=logging.INFO):
        self.logger = app_logger
        self.logger.setLevel(level)

        file_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=3)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(file_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
