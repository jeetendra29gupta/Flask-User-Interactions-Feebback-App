import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from app.config import current_config


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Set up and return a configured logger instance.

    Args:
        name (str, optional): Name of the logger. Defaults to None for root logger.

    Returns:
        logging.Logger: Configured logger instance with file rotation & console output.

    Remarks:
        - Prevents multiple handlers on the same logger if called multiple times.
        - Log files are rotated after reaching max bytes with backup count.
    """
    logger = logging.getLogger(name)
    logger.setLevel(current_config.LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter(current_config.LOG_FORMAT)

        file_handler = RotatingFileHandler(
            current_config.LOG_FILE,
            maxBytes=current_config.MAX_BYTES,
            backupCount=current_config.BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(current_config.LOG_LEVEL)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(current_config.LOG_LEVEL)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
