import logging.handlers
import os
import sys
from common.vars import LOGGING_LEVEL


DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
FILE_PATH = os.path.join(DIR_PATH, 'client_logs.log')

CLIENT_HANDLER = logging.StreamHandler(sys.stderr)
CLIENT_FORMATTER = logging.Formatter('%(asctime)s   %(levelname)-8s %(filename)s : "%(message)s"')
CLIENT_HANDLER.setFormatter(CLIENT_FORMATTER)

FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(FILE_PATH, encoding='utf-8', interval=1, when='D')
FILE_HANDLER.setFormatter(CLIENT_FORMATTER)


CLIENT_LOGGER = logging.getLogger('client')
CLIENT_LOGGER.addHandler(CLIENT_HANDLER)
CLIENT_LOGGER.addHandler(FILE_HANDLER)
CLIENT_LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    CLIENT_LOGGER.info('info message')
    CLIENT_LOGGER.debug('debug message')
    CLIENT_LOGGER.warning('WARNING!')
    CLIENT_LOGGER.critical('SHIT!')
