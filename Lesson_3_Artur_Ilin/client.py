import json
import sys
import time

from socket import AF_INET, socket, SOCK_STREAM
from common.vars import *
from common.utils import get_message, send_message


def create_presence(user_name='Guest'):
    return {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: user_name
        }
    }


def parse_response(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    # client.py 127.0.0.1 8053
    try:
        address = sys.argv[1]
        port = int(sys.argv[2])

        if 65535 < port < 1024:
            raise ValueError
    except IndexError:
        port = DEFAULT_PORT
        address = DEFAULT_IP_ADDRESS
    except ValueError:
        print('Порт не может быть меньше 1024 или больше 65535')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCK.connect((address, port))

    presence_message = create_presence()
    send_message(CLIENT_SOCK, presence_message)

    try:
        response = parse_response(get_message(CLIENT_SOCK))
        print(response)
    except (ValueError, json.JSONDecodeError):
        print('Bad request')


if __name__ == '__main__':
    main()
