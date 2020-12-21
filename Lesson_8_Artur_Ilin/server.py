import argparse
import sys
from select import select

from decos import Log, log
from socket import AF_INET, socket, SOCK_STREAM
from common.variables import *
from common.utils import get_message, send_message

LOGGER = logging.getLogger('server')


@Log()
def get_response_for_message(message, msg_list, client, clients, names):

    LOGGER.debug(f'Разбор сообщения от клиента : {message}')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя занято'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return

    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and \
            TIME in message and SENDER in message and MESSAGE_TEXT in message:
        msg_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(message[ACCOUNT_NAME])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return

    else:
        response = RESPONSE_400
        response[ERROR] = 'Некорректный запрос'
        send_message(client, response)
        return


@log
def parse_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} от {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        LOGGER.error(f'Попытка отправить сообщение незарегистрированному пользоватлю {message[DESTINATION]}')


@log
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serv_address = namespace.addr
    serv_port = namespace.port

    if 65535 < serv_port < 1024:
        LOGGER.critical(f'Укзан недопустимый адрес порта - {serv_port}.'
                        f'Порт может быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    return serv_address, serv_port


def main():
    address, port = parse_args()

    LOGGER.info(f'Запущен сервер. Данные сервера: адрес - {address}, порт - {port}')

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(MAX_CONNECTIONS)
    sock.settimeout(0.5)

    clients = []
    messages = []

    names = {}

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
                recv_data, send_data, err_list = select(clients, clients, err_list, 0)
        except OSError:
            pass

        if recv_data:
            for client in recv_data:
                try:
                    get_response_for_message(get_message(client), messages, client, clients, names)
                except Exception:
                    LOGGER.info(f'Клиент {client} отключился')
                    clients.remove(client)
        for item in messages:
            try:
                parse_message(item, names, send_data)
            except Exception:
                LOGGER.info(f'Связь с клиентом {item[DESTINATION]} потеряна')
                clients.remove(names[item[DESTINATION]])
                del names[item[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
