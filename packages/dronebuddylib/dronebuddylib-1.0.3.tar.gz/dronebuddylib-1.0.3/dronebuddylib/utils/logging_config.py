import logging


def get_logger(log_level=logging.DEBUG):
    logger = logging.getLogger(__name__)
    # Set log level
    logger.setLevel(log_level)
    return logger
