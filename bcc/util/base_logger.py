import logging
import sys

from loguru import logger

log_format = "<lvl> {level} - {message}</lvl>"
logger.remove()  # Remove default logger to avoid dupe logs
logger.add(sys.stderr, format=log_format, level="DEBUG", colorize=True, backtrace=True, diagnose=True)


def get_logger() -> logging.Logger:
    return logger
