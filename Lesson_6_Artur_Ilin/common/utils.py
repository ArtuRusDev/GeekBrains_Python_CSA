import json
from common.vars import *


def get_message(client_sock):
    response_bytes = client_sock.recv(MAX_PACKAGE_LENGTH)
    print(response_bytes)
    if isinstance(response_bytes, bytes):
        response_json = response_bytes.decode(ENCODING)
        response = json.loads(response_json)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    message_json = json.dumps(message)
    message_bytes = message_json.encode(ENCODING)
    sock.send(message_bytes)
