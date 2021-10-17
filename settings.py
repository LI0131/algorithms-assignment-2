import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

LOGGER_FMT = "[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s"
DATE_FMT = "%H:%M:%S"
APP_NAME = __name__
