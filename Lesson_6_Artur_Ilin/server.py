import argparse
import sys
import time
from select import select

from decos import Log
from socket import AF_INET, socket, SOCK_STREAM
from common.vars import *
from common.utils import get_message, send_message

SERVER_LOGGER = logging.getLogger('server')


@Log()
def get_response_for_message(message, msg_list, client):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][
        ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return

    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        msg_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return

    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serv_address = namespace.addr
    serv_port = namespace.port

    if 65535 < serv_port < 1024:
        SERVER_LOGGER.critical(f'Укзан недопустимый адрес порта - {serv_port}.'
                               f'Порт может быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    return serv_address, serv_port


def main():
    address, port = parse_args()

    SERVER_LOGGER.info(f'Запущен сервер. Данные сервера: адрес - {address}, порт - {port}')

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(MAX_CONNECTIONS)
    sock.settimeout(0.5)

    clients = []
    messages = []

    while True:
        try:
            conn, address = sock.accept()
        except OSError:
            pass
        else:
            print(f'Получен запрос на соединение с {str(address)}')
            clients.append(conn)

        recv_data = []
        send_data = []
        err_list = []

        try:
            if clients:
                recv_data, send_data, err_list = select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data:
            for client in recv_data:
                try:
                    get_response_for_message(get_message(client), messages, client)
                except:
                    SERVER_LOGGER.info(f'Клиент {client} отключился')
                    clients.remove(client)
        if messages and send_data:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for wait_client in send_data:
                try:
                    send_message(wait_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {wait_client} отключился')
                    clients.remove(wait_client)


if __name__ == '__main__':
    main()
