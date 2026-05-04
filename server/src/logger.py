import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DEFINITION = os.getenv("LOG_LEVEL", "INFO").upper()

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(module)s] - %(message)s"


def setup_logger():
    """Configure application-wide logging.

    Creates the log directory if it does not exist, configures the root logger
    level from the LOG_LEVEL environment variable and attaches both file and
    console handlers.

    The file handler uses log rotation to prevent unlimited log growth.
    """
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVELS.get(LOG_DEFINITION, logging.INFO))

    formatter = logging.Formatter(LOG_FORMAT)

    handlers = root_logger.handlers[:]
    for handler in handlers:
        root_logger.removeHandler(handler)

    handlers.append(
        RotatingFileHandler(
            os.path.join(log_dir, "app.log"),
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
    )

    handlers.append(
        logging.StreamHandler()
    )

    for handler in handlers:
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
