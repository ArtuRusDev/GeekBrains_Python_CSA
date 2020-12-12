import json
import sys
from decos import log, Log
from socket import AF_INET, socket, SOCK_STREAM
from common.vars import *
from common.utils import get_message, send_message
import log.server_log_config

SERVER_LOGGER = logging.getLogger('server')


@Log()
def get_response_for_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        SERVER_LOGGER.debug(f'Получено сообщение {message} от клиента {message[USER][ACCOUNT_NAME]}')
        response = {RESPONSE: 200}

        SERVER_LOGGER.debug(f'Отправлен ответ {response} клиенту {message[USER][ACCOUNT_NAME]}')
        return response

    SERVER_LOGGER.error(f'Получены некоретные данные от клиента - {message}.')
    response = {RESPONSE: 400, ERROR: 'Bad request'}

    SERVER_LOGGER.debug(f'Отправлен ответ {response} клиенту')
    return response


def main():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if 65535 < port < 1024:
            SERVER_LOGGER.critical(f'Укзан недопустимый адрес порта - {port}.'
                                   f'Порт может быть в диапазоне от 1024 до 65535')
            sys.exit(1)
    except IndexError:
        SERVER_LOGGER.critical(f'Не указан порт. Соединение не удалось')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Порт может быть только в диапазоне от 1024 до 65535. '
                               f'Соединение не удалось')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            address = ''
    except IndexError:
        print('Неообходимо указать адрес после "-p".')
        sys.exit(1)

    SERV_SOCK = socket(AF_INET, SOCK_STREAM)

    SERV_SOCK.bind((address, port))

    SERV_SOCK.listen(MAX_CONNECTIONS)

    while True:
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()
        SERVER_LOGGER.info(f'Установлено соединение с клиетном: {ADDR}')
        try:
            client_message = get_message(CLIENT_SOCK)
            SERVER_LOGGER.info(f'Получено сообщение от клиента: {client_message}')
            response = get_response_for_message(client_message)
            SERVER_LOGGER.debug(f'Сформирован ответ клиенту: {response}')
            send_message(CLIENT_SOCK, response)
            SERVER_LOGGER.info(f'Отправлено сообщение {response} клиенту {ADDR}')
            CLIENT_SOCK.close()
            SERVER_LOGGER.info(f'Соединение с клиентом разорвано')
        except (ValueError, json.JSONDecodeError):
            CLIENT_SOCK.close()
            SERVER_LOGGER.error(f'Получены некоретные данные от клиента {ADDR}. Соединение разорвано')


if __name__ == '__main__':
    main()
