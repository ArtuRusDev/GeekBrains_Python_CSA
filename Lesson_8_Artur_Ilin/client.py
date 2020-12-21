import argparse
import json
import sys
import threading
import time

from decos import log, Log
from socket import AF_INET, socket, SOCK_STREAM
from common.variables import *
from common.utils import get_message, send_message
from errors import ServerError, ReqFieldMissingError, IncorrectDataRecivedError

LOGGER = logging.getLogger('client')


@log
def create_exit_msg(username):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: username
    }


@log
def rcv_msg_from_server(sock, username):
    while True:
        try:
            message = get_message(sock)

            if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message and \
                    MESSAGE_TEXT in message and message[DESTINATION] == username:
                print(f'\nСообщение от {message[SENDER]}: "{message[MESSAGE_TEXT]}"'
                      f'\n>>> ', end='')
                LOGGER.info(f'\nСообщение от {message[SENDER]}: {message[MESSAGE_TEXT]}')
            else:
                LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            LOGGER.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_message(sock, username='Guest'):
    to_user = input('Введите имя получателя: ')
    message = input('Введите ваше сообщение: ')

    new_mes_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        DESTINATION: to_user,
        SENDER: username,
        MESSAGE_TEXT: message
    }
    LOGGER.info(f'Сформировано сообщение для отправки: {new_mes_dict}')

    try:
        send_message(sock, new_mes_dict)
        LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except Exception:
        LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def client_action(sock, username):
    show_help()
    while True:
        command = input('>>> ')
        if command == 'msg':
            create_message(sock, username)
        elif command == 'help':
            show_help()
        elif command == 'exit':
            send_message(sock, create_exit_msg(username))
            print('Завершение соединения')
            LOGGER.info('Завершение соединения')
            time.sleep(0.5)
            break
        else:
            print('Неизвестная команда. Повторите ввод.')


@Log()
def create_presence(user_name='Guest'):
    response = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: user_name
        }
    }

    LOGGER.debug(f'Сформировано сообщение {response} клиенту {response[USER][ACCOUNT_NAME]}')
    return response


def show_help():
    print('    Команды:')
    print('    msg - Написать сообщение.')
    print('    help - Справка по командам')
    print('    exit - Выход')


@log
def parse_response(message):
    LOGGER.debug(f'Разбор сообщения от клиента {message}')

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'

    LOGGER.error(f'Некорректное сообщение от клиента')
    raise ValueError


@log
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serv_address = namespace.addr
    serv_port = namespace.port
    username = namespace.name

    if 65535 < serv_port < 1024:
        LOGGER.critical(
            f'Укзан недопустимый адрес порта - {serv_port}.'
            f'Порт может быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    return serv_address, serv_port, username


def main():
    address, port, username = parse_args()

    if not username:
        username = input('Введите ваше Имя: ')

    LOGGER.info(f'Запущен клинт с именем {username}. Сервер: адрес - {address}, порт - {port}')

    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((address, port))
        send_message(sock, create_presence(username))
        response = parse_response(get_message(sock))
        LOGGER.info(f'Установлено соединение с сервером. Получен ответ: {response}')
        print('Установлено соединение с сервером')
    except json.JSONDecodeError:
        LOGGER.error('Не удалось декодировать строку.')
        sys.exit(1)
    except ServerError as e:
        LOGGER.error(f'Сервер вернул ошибку: {e.text}')
        sys.exit(1)
    except ReqFieldMissingError as miss_err:
        LOGGER.error(f'Отсутствует необходимое поле в ответе сервера: {miss_err.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER.critical(f'Ошибка при подключении к серверу {address}:{port}')
        sys.exit(1)
    else:

        print(f'Клиент - {username}')
        # Демон для приема сообщений
        receiver = threading.Thread(target=rcv_msg_from_server, args=(sock, username))
        receiver.daemon = True
        receiver.start()

        # Демон для обработки действий пользователя
        client_action_env = threading.Thread(target=client_action, args=(sock, username))
        client_action_env.daemon = True
        client_action_env.start()

        while True:
            time.sleep(1)
            if receiver.is_alive() and client_action_env.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
