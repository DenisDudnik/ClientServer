import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.const import ACCOUNT_NAME, ACTION, PRESENCE, TIME, USER, ALERT, RESPONSE, ERROR
from client import create_presence, process_answer

class TestClient(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_presence(self):
        msg = create_presence(account_name='client1', status='I am here!')
        msg[TIME] = 1.1

        good_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            "type": "status",
            USER: {
                ACCOUNT_NAME: 'client1',
                "status": 'I am here!'
            }
        }

        self.assertEqual(msg, good_msg)
    
    def test_create_presence_default(self):
        msg = create_presence()
        msg[TIME] = 1.1

        good_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            "type": "status",
            USER: {
                ACCOUNT_NAME: 'guest',
                "status": ''
            }
        }

        self.assertEqual(msg, good_msg)

    def test_process_answer_200(self):
        msg = {
            RESPONSE: 200,
            ALERT: "OK"
        }

        self.assertEqual(process_answer(msg), '200: OK')
    
    def test_process_answer_400(self):
        msg = {
            RESPONSE: 400,
            ERROR: "Bad Request"
        }

        self.assertEqual(process_answer(msg), '400: Bad Request')
    
    def test_process_answer_no_response(self):
        msg = {}

        with self.assertRaises(ValueError):
            process_answer(msg)

if __name__ == '__main__':
    unittest.main()