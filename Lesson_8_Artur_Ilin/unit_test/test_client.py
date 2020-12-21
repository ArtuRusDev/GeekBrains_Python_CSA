from client import parse_response, create_presence
import unittest

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestClient(unittest.TestCase):
    def test_parse_response_correct(self):
        self.assertEqual(parse_response({RESPONSE: 200}), '200 : OK')

    def test_parse_response_400(self):
        self.assertEqual(parse_response({RESPONSE: 404, ERROR: 'Not found'}), '400 : Not found')

    def test_parse_response_bad_input(self):
        with self.assertRaises(ValueError):
            parse_response({ERROR: 'Not found'})

    def test_create_presence(self):
        response = create_presence()
        response[TIME] = '1'
        self.assertEqual(response, {ACTION: PRESENCE, TIME: '1', USER: {ACCOUNT_NAME: 'Guest'}})


if __name__ == '__main__':
    unittest.main()
