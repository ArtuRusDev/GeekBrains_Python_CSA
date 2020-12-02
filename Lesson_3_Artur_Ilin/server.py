import json
import sys
from socket import AF_INET, socket, SOCK_STREAM
from common.vars import *
from common.utils import get_message, send_message


def get_response_for_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {
            RESPONSE: 200
        }
    return {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }


def main():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if 65535 < port < 1024:
            raise ValueError
    except IndexError:
        print('Неообходимо указать номер порта после "-p".')
        sys.exit(1)
    except ValueError:
        print('Порт не может быть меньше 1024 или больше 65535')
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
        try:
            client_message = get_message(CLIENT_SOCK)
            print(client_message)
            response = get_response_for_message(client_message)
            send_message(CLIENT_SOCK, response)
            CLIENT_SOCK.close()
        except (ValueError, json.JSONDecodeError):
            print('Bad request')
            CLIENT_SOCK.close()


if __name__ == '__main__':
    main()
