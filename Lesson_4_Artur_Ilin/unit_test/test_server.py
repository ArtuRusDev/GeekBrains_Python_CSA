from server import get_response_for_message
from common.vars import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
import unittest
import time


class TestServer(unittest.TestCase):
    bad_response = {RESPONSE: 400, ERROR: 'Bad request'}
    ok_response = {RESPONSE: 200}

    def test_correct(self):
        """ Тест с валидными данными """
        self.assertEqual(
            get_response_for_message({ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: 'Guest'}}),
            self.ok_response
        )

    def test_without_action(self):
        """ Тест без параметра ACTION """
        self.assertEqual(
            get_response_for_message({TIME: time.time(), USER: {ACCOUNT_NAME: 'Guest'}}), self.bad_response)

    def test_without_time(self):
        """ Тест без параметра TIME """
        self.assertEqual(
            get_response_for_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.bad_response)

    def test_without_user(self):
        """ Тест без параметра USER """
        self.assertEqual(get_response_for_message({ACTION: PRESENCE, TIME: time.time()}), self.bad_response)

    def test_unknown_user(self):
        """ Пользователь, отличный от 'Guest' """
        self.assertEqual(
            get_response_for_message({ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: 'Alex'}}),
            self.bad_response
        )

    def test_unknown_action(self):
        """ Поле ACTION со значением отличным от PRESENCE """
        self.assertEqual(
            get_response_for_message({ACTION: 'TEST', TIME: time.time(), USER: {ACCOUNT_NAME: 'Alex'}}),
            self.bad_response
        )


if __name__ == '__main__':
    unittest.main()
