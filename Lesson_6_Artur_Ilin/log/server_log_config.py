import logging.handlers
import os
import sys
from common.vars import LOGGING_LEVEL

DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
FILE_PATH = os.path.join(DIR_PATH, 'server_logs.log')

SERVER_HANDLER = logging.StreamHandler(sys.stderr)
SERVER_FORMATTER = logging.Formatter('%(asctime)s   %(levelname)-8s %(filename)s : "%(message)s"')
SERVER_HANDLER.setFormatter(SERVER_FORMATTER)

FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(FILE_PATH, encoding='utf-8', interval=1, when='D')
FILE_HANDLER.setFormatter(SERVER_FORMATTER)

SERVER_LOGGER = logging.getLogger('server')
SERVER_LOGGER.addHandler(SERVER_HANDLER)
SERVER_LOGGER.addHandler(FILE_HANDLER)
SERVER_LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    SERVER_LOGGER.info('info message')
    SERVER_LOGGER.debug('debug message')
    SERVER_LOGGER.warning('warning message')
    SERVER_LOGGER.critical('SHIT!')
