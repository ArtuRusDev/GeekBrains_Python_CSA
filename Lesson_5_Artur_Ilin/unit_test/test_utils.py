import json
import unittest
from common.utils import get_message, send_message
from common.vars import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class Socket:
    def __init__(self, base_dict):
        self.base_dict = base_dict
        self.encoded_data = None
        self.recv_data = None

    def send(self, message):
        json_message = json.dumps(self.base_dict)
        self.encoded_data = json_message.encode('utf-8')
        self.recv_data = message

    def recv(self, max_mes_len):
        get_data = json.dumps(self.base_dict)
        return get_data.encode('utf-8')


class TestUtils(unittest.TestCase):
    dict_for_send = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }
    bad_response = {RESPONSE: 400, ERROR: 'Bad request'}
    ok_response = {RESPONSE: 200}

    def test_send_message(self):
        socket = Socket(self.dict_for_send)
        send_message(socket, self.dict_for_send)
        self.assertEqual(socket.encoded_data, socket.recv_data)

        with self.assertRaises(Exception):
            send_message(socket, socket)

    def test_get_message(self):
        socket_ok = Socket(self.ok_response)
        socket_bad = Socket(self.bad_response)

        self.assertEqual(get_message(socket_ok), self.ok_response)
        self.assertEqual(get_message(socket_bad), self.bad_response)


if __name__ == '__main__':
    unittest.main()
