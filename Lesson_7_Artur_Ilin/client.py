import argparse
import json
import sys
import time
from decos import log, Log
from socket import AF_INET, socket, SOCK_STREAM
from common.vars import *
from common.utils import get_message, send_message
from errors import ServerError, ReqFieldMissingError

CLIENT_LOGGER = logging.getLogger('client')


@log
def parse_msg_from_serv(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от клиента {message[SENDER]} - {message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от клиента {message[SENDER]} - {message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера - {message}')


@log
def create_message(sock, user_name='Guest'):
    message = input('Введите ваше сообщение (введите *** для выхода): ')
    if message == '***':
        sock.close()
        CLIENT_LOGGER.info(f'Выход по команде пользователя')
        print('Завершение работы...')
        sys.exit(0)
    new_mes_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: user_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.info(f'Сформировано сообщение для отправки: {new_mes_dict}')

    return new_mes_dict


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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serv_address = namespace.addr
    serv_port = namespace.port
    client_mode = namespace.mode

    if 65535 < serv_port < 1024:
        CLIENT_LOGGER.critical(f'Укзан недопустимый адрес порта - {serv_port}.'
                               f'Порт может быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Укзан недопустимый режим - {client_mode}.'
                               f'Режим должне быть "listen" или "send"')
        sys.exit(1)

    return serv_address, serv_port, client_mode


def main():
    address, port, mode = parse_args()
    CLIENT_LOGGER.info(f'Запущен клиент с режимом {mode}.\n Данные сервера: адрес - {address}, порт - {port}\n')

    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((address, port))
        send_message(sock, create_presence())
        response = parse_response(get_message(sock))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Получен ответ: {response}')
        print('Установлено соединение с сервером')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать строку.')
        sys.exit(1)
    except ServerError as e:
        CLIENT_LOGGER.error(f'Сервер вернул ошибку: {e.text}')
        sys.exit(1)
    except ReqFieldMissingError as miss_err:
        CLIENT_LOGGER.error(f'Отсутствует необходимое поле в ответе сервера: {miss_err.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Ошибка при подключении к серверу {address}:{port}')
        sys.exit(1)
    else:
        if mode == 'send':
            print('Режим - Отправка сообщений')
        else:
            print('Режим - Получение сообщений')
        while True:
            if mode == 'send':
                try:
                    send_message(sock, create_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {address} потеряно')
                    sys.exit(1)

            if mode == 'listen':
                try:
                    (sock, get_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {address} потеряно')
                    sys.exit(1)


if __name__ == '__main__':
    main()
