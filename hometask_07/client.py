'''
Программа-клиент.
Можно запускать скрипт из командной строки с параметрами:

python client.py 127.0.0.1 7777 -m (send|listen)

Либо адрес порт будут по умолчанию, а режим работы клиента
будет запрошен у пользователя.
'''

import logging
import sys
from socket import AF_INET, SOCK_STREAM, socket

import log.client_log_config
from common.utils import msg_timestamp, recv_msg, send_msg
from common.variables import (ACCOUNT_NAME, ACTION, AUTHENTICATE, DEFAULT_ADDR,
                            DEFAULT_PORT, FROM, MESSAGE_TEXT, MSG, PASSWORD,
                            PRESENCE, TIME, USER)

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
        if addr != '-m':
            CLIENT_LOGGER.debug('В параметрах запуска скрипта передан адрес: %s', addr)
        else:
            addr = DEFAULT_ADDR
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
def get_mode():
    '''
    Функция получает режим работы клиента из командной строки
    или запрашивает его у пользователя
    '''
    if '-m' in sys.argv:
        m_key_index = sys.argv.index('-m')
        mode_index = m_key_index + 1
        mode = sys.argv[mode_index]
        CLIENT_LOGGER.debug('В параметрах запуска скрипта передан режим '
                            'работы клиента: %s', mode)
    else:
        while True:
            mode = input('Введите режим работы клиента (l - listen, s - send), q - выход: ')
            if mode == 'l':
                mode = 'listen'
                break
            elif mode == 's':
                mode = 'send'
                break
            elif mode == 'q':
                CLIENT_LOGGER.info('Завершение работы по команде пользователя')
                print('Завершение работы по команде пользователя')
                input('Для выхода нажмите Enter')
                sys.exit(0)
            else:
                continue

        CLIENT_LOGGER.debug('Назначен режим работы клиента: %s', mode) 
    CLIENT_LOGGER.info('Режим работы клиента: %s', mode)
    return mode


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


@log
def create_message(sock, account_name='Guest'):
    '''Функция запрашивает сообщение для отправки'''
    input_msg = input('Введите сообщение для отправки, q - для выхода: ')
    if input_msg == 'q':
        CLIENT_LOGGER.info(f'Завершение работы клиента {sock.getsockname()} по команде пользователя')
        sock.close()
        print('Завершение работы по команде пользователя')
        input('Для выхода нажмите Enter')
        sys.exit(0)
    else:
        msg_to_send_json = {
            ACTION: MSG,
            TIME: msg_timestamp(),
            FROM: account_name,
            MESSAGE_TEXT: input_msg
        }
    CLIENT_LOGGER.debug(f'Сформировано сообщение для отправки: {msg_to_send_json}')
    return msg_to_send_json


@log
def get_msg_from_server(sock):
    msg_from_server = recv_msg(sock)
    if ACTION in msg_from_server and msg_from_server[ACTION] == MSG \
            and FROM in msg_from_server and MESSAGE_TEXT in msg_from_server:
        print(f'Получено сообщение от пользователя {msg_from_server[FROM]}: '
                f'{msg_from_server[MESSAGE_TEXT]}')
    else:
        print(f'Получено некооректное сообщение от сервера: {msg_from_server}')
        CLIENT_LOGGER.info(f'Получено некооректное сообщение от сервера: {msg_from_server}')



def main():

    # Получаем адрес сервера и порт для подключения,
    # а также режим работы клиента из параметров запуска скрипта
    # или дефолтные значения (режим работы клиента в этом случае
    # нужно ввести вручную)
    serv_addr = get_addr()
    serv_port = get_port()
    client_mode = get_mode()
    
    print(f'Запущен клиент с параметрами: адрес сервера {serv_addr}, '
        f'порт сервера {serv_port}, режим клиента {client_mode}')
    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: адрес сервера {serv_addr}, '
        f'порт сервера {serv_port}, режим клиента {client_mode}')
    
    # Пытаемся подключиться к серверу
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((serv_addr, serv_port))
        print(f'Установлено подключение на адрес {serv_addr} порт {serv_port}')
        CLIENT_LOGGER.info('Установлено подключение на адрес %s порт %d', serv_addr, serv_port)
    except Exception as e:
        # print('Возникло исключение:', e)
        input('Нажмите Enter для выхода из программы')
        sys.exit(1)
    # Если подключение успешно
    else:
        # Отправляем сообщение PRESENCE
        msg_to_server = msg_presence(account_name='Guest')
        send_msg(sock, msg_to_server)
        print(f'Отправлено сообщение {msg_to_server}')
        CLIENT_LOGGER.info('Отправлено сообщение %s', msg_to_server)

        # Получаем ответ от сервера
        msg_from_server = recv_msg(sock)
        print(f'Получено сообщение: {msg_from_server}')
        CLIENT_LOGGER.info('Получено сообщение: %s', msg_from_server)

        # В бесконечном цикле либо отправляем, либо принимаем сообщения
        while True:
            if client_mode == 'send':  # Только отправляем сообщения
                try:
                    msg_to_server = create_message(sock, account_name='Guest')
                    send_msg(sock, msg_to_server)
                except Exception as e:
                    sock.close()
                    print('Возникло исключение:', e)
                    input('Для выхода нажмите Enter')
                    sys.exit(1)
            elif client_mode == 'listen':  # Только принимаем сообщения
                try:
                    get_msg_from_server(sock)
                except Exception as e:
                    sock.close()
                    print('Возникло исключение:', e)
                    input('Для выхода нажмите Enter')
                    sys.exit(1)
            else:
                print('Недопустимый режим работы клиента')
                input('Для выхода нажмите Enter')
                sys.exit(0)


if __name__ == '__main__':
    main()
