import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))

import unittest

from client import get_addr, get_port, msg_auth, msg_presence

from common.variables import AUTHENTICATE, PASSWORD, DEFAULT_ADDR, DEFAULT_PORT, \
    ACCOUNT_NAME, ACTION, USER, TIME, PRESENCE


class TestClient(unittest.TestCase):
    def test_get_addr_default_addr(self):
        '''Тест get_addr() с дефолтным адресом'''
        sys.argv = ['']
        result = get_addr()
        self.assertEqual(result, DEFAULT_ADDR)
    
    def test_get_addr_given_addr(self):
        '''Тест get_addr() с переданным адресом'''
        sys.argv = ['', '0.0.0.0', 9999]
        result = get_addr()
        self.assertEqual(result, '0.0.0.0')
    
    def test_get_port_default_port(self):
        '''Тест get_port() с дефолтным портом'''
        sys.argv = ['']
        result = get_port()
        self.assertEqual(result, DEFAULT_PORT)
    
    def test_get_port_given_port(self):
        '''Тест get_port() с переданным портом'''
        sys.argv = ['', '0.0.0.0', 9999]
        result = get_port()
        self.assertEqual(result, 9999)

    def test_msg_presence_default_name(self):
        '''Test msg_presence() с дефолтным account_name=Guest'''
        result = msg_presence()
        result[TIME] = 123
        self.assertEqual(result, {ACTION: PRESENCE, TIME: 123,\
            USER: {ACCOUNT_NAME: 'Guest'}})
    
    def test_msg_presence_given_name(self):
        '''Test msg_presence() с переданным account_name=Mary'''
        result = msg_presence('Mary')
        result[TIME] = 123
        self.assertEqual(result, {ACTION: PRESENCE, TIME: 123,\
            USER: {ACCOUNT_NAME: 'Mary'}})

    def test_msg_auth_default_name_password(self):
        '''Тест msg_auth() с дефолтными account_name="John" и password="passw0rd"'''
        result = msg_auth()
        result[TIME] = 123
        self.assertEqual(result, {ACTION: AUTHENTICATE, TIME: 123, \
            USER: {ACCOUNT_NAME: 'John', PASSWORD: 'passw0rd'}})
    
    def test_msg_auth_given_name_password(self):
        '''Тест msg_auth() с переданными account_name="Mary" и password="ladymary"'''
        result = msg_auth(account_name="Mary", password="ladymary")
        result[TIME] = 123
        self.assertEqual(result, {ACTION: AUTHENTICATE, TIME: 123, \
            USER: {ACCOUNT_NAME: 'Mary', PASSWORD: 'ladymary'}})
    

if __name__ == '__main__':
    unittest.main()
