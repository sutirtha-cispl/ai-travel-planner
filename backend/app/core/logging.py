"""Centralized logging configuration."""

import logging
import sys

from app.config.settings import settings

LOGGING_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging() -> None:
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(level)
