'''
Программа-клиент.
Запускать скрипт из командной строки с параметрами:
python client.py 127.0.0.1 7777.
'''

# TODO Сделать выбор отправляемого сообщения - запрос в бесконечном цикле,
# выход по q

import logging
import sys
from socket import AF_INET, SOCK_STREAM, socket

import log.client_log_config
from common.utils import msg_timestamp, recv_msg, send_msg
from common.variables import (ACCOUNT_NAME, ACTION, AUTHENTICATE, DEFAULT_ADDR,
                              DEFAULT_PORT, PASSWORD, PRESENCE, TIME, USER)

from decos import log


# Получаем клиентский логгер из 'log.client_log_config'
CLIENT_LOGGER = logging.getLogger('client_logger')

@log
def get_addr():
    '''
    Функция получает адрес сервера из командной строки
    или возращает дефолтное значение'''
    try:
        addr = sys.argv[1]
        CLIENT_LOGGER.debug('В параметрах запуска скрипта передан адрес: %s', addr)
    except IndexError:
        addr = DEFAULT_ADDR
        CLIENT_LOGGER.debug('В параметрах запуска скрипта не передан адрес, '
                            'назначен адрес по умолчанию: %s', addr)
    CLIENT_LOGGER.info('Адрес для подключения: %s', addr)
    return addr


@log
def get_port():
    '''
    Функция получает порт из командной строки
    или возращает дефолтное значение'''
    try:
        port = int(sys.argv[2])
        CLIENT_LOGGER.debug('В параметрах запуска скрипта передан порт: %d', port)
    except (IndexError, ValueError):
        port = DEFAULT_PORT
        CLIENT_LOGGER.debug('В параметрах запуска скрипта не передан порт, '
                            'назначен порт по умолчанию: %d', port)
    CLIENT_LOGGER.info('Порт для подключения: %d', port)
    return port


@log
def msg_presence(account_name='Guest'):
    '''Функция отправки сообщения PRESENCE'''
    msg_to_server_json = {
        ACTION: PRESENCE,
        TIME: msg_timestamp(),
        USER: {
            ACCOUNT_NAME: account_name,
        }
    }
    CLIENT_LOGGER.info('Сообщение для отправки на сервер: %s', msg_to_server_json)
    return msg_to_server_json


@log
def msg_auth(account_name='John', password='passw0rd'):
    '''Функция отправки сообщения AUTHENTICATE'''
    msg_to_server_json = {
        ACTION: AUTHENTICATE,
        TIME: msg_timestamp(),
        USER: {
            ACCOUNT_NAME: account_name,
            PASSWORD: password,
        }
    }
    CLIENT_LOGGER.info('Сообщение для отправки на сервер: %s', msg_to_server_json)
    return msg_to_server_json



def main():

    # Получаем адрес и порт для прослушивания
    # из параметров запуска скрипта
    # или дефолтные значения
    serv_addr = get_addr()
    serv_port = get_port()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((serv_addr, serv_port))
    print(f'Установлено подключение на адрес {serv_addr} порт {serv_port}')
    CLIENT_LOGGER.info('Установлено подключение на адрес %s порт %d', serv_addr, serv_port)
    
    # Отправляем сообщение PRESENCE
    msg_to_server = msg_presence(account_name='Guest')
    send_msg(sock, msg_to_server)
    print(f'Отправлено сообщение {msg_to_server}')
    CLIENT_LOGGER.info('Отправлено сообщение %s', msg_to_server)

    msg_from_server = recv_msg(sock)
    print(f'Получено сообщение: {msg_from_server}')
    CLIENT_LOGGER.info('Получено сообщение: %s', msg_from_server)

    if sock:
        sock.close()

    print('==========')

    # Создаю подключение к серверу второй раз,
    # чтобы отправить другое сообщение - для проверки

    # Получаем адрес и порт для прослушивания
    # из параметров запуска скрипта
    # или дефолтные значения
    serv_addr = get_addr()
    serv_port = get_port()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((serv_addr, serv_port))
    print(f'Установлено подключение на адрес {serv_addr} порт {serv_port}')
    CLIENT_LOGGER.info('Установлено подключение на адрес %s порт %d', serv_addr, serv_port)


    # Отправляем сообщение AUTHENTICATE - для проверки получения ошибки
    msg_to_server = msg_auth(account_name='John', password='passw0rd')
    send_msg(sock, msg_to_server)
    print(f'Отправлено сообщение {msg_to_server}')
    CLIENT_LOGGER.info('Отправлено сообщение %s', msg_to_server)

    msg_from_server = recv_msg(sock)
    print(f'Получено сообщение: {msg_from_server}')
    CLIENT_LOGGER.info('Получено сообщение: %s', msg_from_server)
    
    if sock:
        sock.close()


if __name__ == '__main__':
    main()
