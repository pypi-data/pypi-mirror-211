import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Union

from dotenv import load_dotenv

from .CustomFormatter import CoolFormatter

# Define the default logging level
DEFAULT_LOGGING_LEVEL = logging.INFO
load_dotenv()

ROOT_DIR = os.getenv('ROOT_DIR')

# Check if ROOT_DIR is set
if ROOT_DIR is None:
    raise Exception("The ROOT_DIR environment variable must be set.")

# Define the default log directory
DEFAULT_LOG_DIR = os.path.join(ROOT_DIR, 'logs')

class LoggerSingleton:
    __instance: 'LoggerSingleton' = None
    __log_level: int = DEFAULT_LOGGING_LEVEL
    __log_dir: str = DEFAULT_LOG_DIR

    @classmethod
    def get_instance(cls) -> 'LoggerSingleton':
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self) -> None:
        self.loggers = {}

    # New setter method for changing log level
    def set_level(self, level: int) -> None:
        self.__log_level = level

    # New setter method for changing log directory
    def set_log_dir(self, dir_path: str) -> None:
        self.__log_dir = os.path.join(dir_path, 'logs')
        if not os.path.exists(self.__log_dir):
            os.makedirs(self.__log_dir)

    def get_console_handler(self) -> logging.StreamHandler:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.get_formatter())
        return console_handler

    def get_file_handler(self) -> TimedRotatingFileHandler:
        file_handler = TimedRotatingFileHandler(os.path.join(self.__log_dir, 'logs.log'), when='midnight')
        file_handler.setFormatter(self.get_file_formatter())
        return file_handler

    def get_formatter(self) -> CoolFormatter:
        return CoolFormatter()

    def get_file_formatter(self) -> logging.Formatter:
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def get_logger(self, logger_name: str) -> logging.Logger:
        if logger_name in self.loggers:
            return self.loggers[logger_name]

        logger = logging.getLogger(logger_name)
        logger.setLevel(self.__log_level)  # Use the current log level
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False

        self.loggers[logger_name] = logger
        return logger


def get_logger(logger_name: str) -> logging.Logger:
    return LoggerSingleton.get_instance().get_logger(logger_name)


# New utility methods
def set_log_level(level: int) -> None:
    LoggerSingleton.get_instance().set_level(level)


def set_log_dir(dir_path: str) -> None:
    LoggerSingleton.get_instance().set_log_dir(dir_path)
