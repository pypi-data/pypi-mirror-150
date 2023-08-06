import logging

from pypitools import LOGGER_NAME


def get_logger():
    return logging.getLogger(LOGGER_NAME)
