import sys
import os
from unittest import result
sys.path.append(os.path.join(os.getcwd(), '..'))

import unittest

from server import get_addr, get_port, generate_msg_to_client

from common.variables import ALERT, AUTHENTICATE, ERROR, PASSWORD, \
    DEFAULT_ADDR, DEFAULT_PORT, ACCOUNT_NAME, ACTION, RESPONSE, USER, \
    TIME, PRESENCE


class TestServer(unittest.TestCase):
    def test_get_addr_default_addr(self):
        '''Тест get_addr() с дефолтным адресом'''
        sys.argv = ['']
        result = get_addr()
        self.assertEqual(result, DEFAULT_ADDR)
    
    def test_get_addr_given_addr(self):
        '''Тест get_addr() с переданным адресом'''
        sys.argv = ['', '-a', '0.0.0.0', '-p', 9999]
        result = get_addr()
        self.assertEqual(result, '0.0.0.0')
    
    def test_get_port_default_port(self):
        '''Тест get_port() с дефолтным портом'''
        sys.argv = ['']
        result = get_port()
        self.assertEqual(result, DEFAULT_PORT)
    
    def test_get_port_given_port(self):
        '''Тест get_port() с переданным портом'''
        sys.argv = ['', '-a', '0.0.0.0', '-p', 9999]
        result = get_port()
        self.assertEqual(result, 9999)
    
    def test_generate_msg_to_client_recv_presence(self):
        '''Тест generate_msg_to_client() при получении PRESENCE'''
        msg_to_server_json = {
            ACTION: PRESENCE,
            TIME: 123,
            USER: {
                ACCOUNT_NAME: 'Guest',
            }
        }
        result = generate_msg_to_client(msg_to_server_json)
        result[TIME] = 123
        self.assertEqual(result, {RESPONSE: 200, ALERT: 'OK', TIME: 123})
    
    def test_generate_msg_to_client_recv_auth(self):
        '''Тест generate_msg_to_client() при получении AUTHENTICATE'''
        msg_to_server_json = {
            ACTION: AUTHENTICATE,
            TIME: 123,
            USER: {
                ACCOUNT_NAME: 'John',
                PASSWORD: 'passw0rd',
            }
        }
        result = generate_msg_to_client(msg_to_server_json)
        result[TIME] = 123
        self.assertEqual(result, {RESPONSE: 400, ERROR: 'Bad request', TIME: 123})

if __name__ == '__main__':
    unittest.main()
