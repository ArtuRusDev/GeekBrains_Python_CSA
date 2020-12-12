import json
import sys
import time
import log.client_log_config
from decos import log, Log
from socket import AF_INET, socket, SOCK_STREAM
from common.vars import *
from common.utils import get_message, send_message

CLIENT_LOGGER = logging.getLogger('client')


@Log()
def create_presence(user_name='Guest'):
    response = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: user_name
        }
    }

    CLIENT_LOGGER.debug(f'Сформировано сообщение {response} клиенту {response[USER][ACCOUNT_NAME]}')
    return response


def parse_response(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от клиента {message}')

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'

    CLIENT_LOGGER.error(f'Некорректное сообщение от клиента')
    raise ValueError


def main():
    # client.py 127.0.0.1 8053
    try:
        address = sys.argv[1]
        port = int(sys.argv[2])

        if 65535 < port < 1024:
            CLIENT_LOGGER.error(f'Укзан недопустимый адрес порта - {port}.'
                                f'Порт может быть в диапазоне от 1024 до 65535')
            sys.exit(1)
    except IndexError:
        port = DEFAULT_PORT
        address = DEFAULT_IP_ADDRESS
    except ValueError:
        print('Порт не может быть меньше 1024 или больше 65535')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCK.connect((address, port))
    CLIENT_LOGGER.debug(f'Установлено соединение с клиентном {address}')

    presence_message = create_presence()
    send_message(CLIENT_SOCK, presence_message)
    CLIENT_LOGGER.debug(f'Отправлено сообщение клиенту {presence_message}')

    try:
        response = parse_response(get_message(CLIENT_SOCK))
        CLIENT_LOGGER.debug(f'Получено сообщение от клиента - {response}')

    except (ValueError, json.JSONDecodeError):
        CLIENT_LOGGER.debug(f'Некорректный запрос от клиента')


if __name__ == '__main__':
    main()
