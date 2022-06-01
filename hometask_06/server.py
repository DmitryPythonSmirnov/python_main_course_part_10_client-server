'''
Сервер
'''

# TODO Сделать перехват Ctrl+C для остановки сервера

import logging
import sys
from socket import AF_INET, SOCK_STREAM, socket

import log.server_log_config
from common.utils import msg_timestamp, recv_msg, send_msg
from common.variables import (ACTION, ALERT, DEFAULT_ADDR, DEFAULT_PORT, ERROR,
                              MAX_CONNECTIONS, PRESENCE, RESPONSE, TIME)

from decos import log


# Получаем серверный логгер из 'log.server_log_config'
SERVER_LOGGER = logging.getLogger('server_logger')


@log
def get_addr():
    '''
    Функция получает адрес сервера из командной строки
    или возращает дефолтное значение'''
    if '-a' in sys.argv:
        a_key_index = sys.argv.index('-a')
        addr_index = a_key_index + 1
        addr = sys.argv[addr_index]
        SERVER_LOGGER.debug('В параметрах запуска скрипта передан адрес '
                            'для прослушивания: %s', addr)
    else:
        addr = DEFAULT_ADDR
        SERVER_LOGGER.debug('Назначен адрес для прослушивания по умолчанию: %s', addr)
    
    SERVER_LOGGER.info('Адрес для прослушивания: %s', addr)
    return addr


@log
def get_port():
    '''
    Функция получает порт из командной строки
    или возращает дефолтное значение'''
    if '-p' in sys.argv:
        p_key_index = sys.argv.index('-p')
        port_index = p_key_index + 1
        port = int(sys.argv[port_index])
        SERVER_LOGGER.debug('В парамтерах запуска скрипта передан порт '
                            'для прослушивания: %d', port)
    else:
        port = DEFAULT_PORT
        SERVER_LOGGER.debug('Назначен порт для прослушивания '
                            'по умолчанию: %d', port)
    SERVER_LOGGER.info('Порт для прослушивания: %d', port)
    return port


@log
def generate_msg_to_client(msg_from_client_json):
    msg_to_client_json = {}
    if ACTION in msg_from_client_json and msg_from_client_json['action'] == PRESENCE:
        msg_to_client_json[RESPONSE] = 200
        msg_to_client_json[ALERT] = 'OK'
        SERVER_LOGGER.info('Сформировано сообщение клиенту: %s',
                        msg_to_client_json)
    else:
        msg_to_client_json[RESPONSE] = 400
        msg_to_client_json[ERROR] = 'Bad request'
        SERVER_LOGGER.warning('Получен неверный запрос от клиента. '
                    'Сообщение для отправки клиенту: %s', msg_to_client_json)
    
    msg_to_client_json[TIME] = msg_timestamp()
    return msg_to_client_json


def main():
    
    # Получаем адрес и порт для прослушивания
    # из параметров запуска скрипта
    # или дефолтные значения
    serv_addr = get_addr()
    serv_port = get_port()

    # Создаём серверный сокет
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((serv_addr, serv_port))
    print(f'Сервер запущен. Адрес: {serv_addr}, порт: {serv_port}')
    SERVER_LOGGER.info('Сервер запущен. Адрес: %s, порт: %d', serv_addr, serv_port)
    sock.listen(MAX_CONNECTIONS)

    while True:
        client_connection, client_addr = sock.accept()
        msg_from_client_json = recv_msg(client_connection)
        print(f'Получено от клиента {client_addr}: {msg_from_client_json}')
        SERVER_LOGGER.info('Получено от клиента %s: %s', client_addr, msg_from_client_json)

        msg_to_client_json =  generate_msg_to_client(msg_from_client_json)
        send_msg(client_connection, msg_to_client_json)
        print(f'Отправлено клиенту {client_addr}: {msg_to_client_json}')
        SERVER_LOGGER.info('Отправлено сообщение клиенту %s: %s', client_addr, msg_to_client_json)

        if client_connection:
            client_connection.close()


if __name__ == '__main__':
    main()
