import logging

DEFAULT_PORT = 7777
DEFAULT_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 1024

ENCODING = 'utf-8'

# JIM протокол
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'

# Другие ключи
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'


LOGGING_LEVEL = logging.DEBUG
