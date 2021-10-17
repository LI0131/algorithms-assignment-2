import logging

import settings

BASIC_CONFIG = {
    'level': settings.LOG_LEVEL,
    'format': settings.LOGGER_FMT,
    'datefmt': settings.DATE_FMT
}


def init_logger():
    logging.basicConfig(**BASIC_CONFIG)
    return logging.getLogger(settings.APP_NAME)
