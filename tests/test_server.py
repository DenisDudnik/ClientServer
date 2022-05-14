import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from server import create_response
from utils.const import RESPONSE, ALERT, ERROR, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME


class TestServer(unittest.TestCase):
    msg_ok = {
            RESPONSE: 200,
            ALERT: "OK"
        }

    msg_bad = {
            RESPONSE: 400,
            ERROR: "Bad Request"
        }
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_response_ok(self):
        msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            "type": "status",
            USER: {
                ACCOUNT_NAME: 'client1',
                "status": 'I am here!'
            }
        }
        self.assertEqual(create_response(msg), self.msg_ok)

    def test_create_response_wrong_action(self):
        msg = {
            ACTION: 'UNKNOWN',
            TIME: 1.1,
            "type": "status",
            USER: {
                ACCOUNT_NAME: 'client1',
                "status": 'I am here!'
            }
        }
        self.assertEqual(create_response(msg), self.msg_bad)
    
    def test_create_response_no_action(self):
        msg = {
            TIME: 1.1,
            "type": "status",
            USER: {
                ACCOUNT_NAME: 'client1',
                "status": 'I am here!'
            }
        }
        self.assertEqual(create_response(msg), self.msg_bad)
    
    def test_create_response_no_time(self):
        msg = {
            ACTION: PRESENCE,
            "type": "status",
            USER: {
                ACCOUNT_NAME: 'client1',
                "status": 'I am here!'
            }
        }
        self.assertEqual(create_response(msg), self.msg_bad)

    def test_create_response_no_user(self):
        msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            "type": "status",
        }
        self.assertEqual(create_response(msg), self.msg_bad)

    def test_create_response_wrong_user(self):
        msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            "type": "status",
            USER: {
                ACCOUNT_NAME: 'client2',
                "status": 'I am here!'
            }
        }
        self.assertEqual(create_response(msg), self.msg_bad)


if __name__ == '__main__':
    unittest.main()