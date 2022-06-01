'''
Модуль с общими функциями
'''

import json
import time
from .variables import ENCODING


def send_msg(conn, msg_json):
    '''Функция отправки сообщения клиенту или серверу'''
    conn.send(json.dumps(msg_json).encode(ENCODING))


def recv_msg(conn):
    '''
    Функция получения сообщения от клиента или сервера.
    Возвращает сообщение об ошибке или JSON-объект.
    '''
    msg_bytes = conn.recv(1024)
    try:
        msg_json = json.loads(msg_bytes.decode('utf-8'))
    except TypeError:
        return 'Принятое сообщение не удалось преобразовать в JSON-объект'
    else:
        return msg_json


def msg_timestamp():
    '''Функция возвращает Unix time'''
    return int(time.time())
