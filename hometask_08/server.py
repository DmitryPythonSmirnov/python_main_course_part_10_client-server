'''
Сервер
'''


import logging
import sys
import select
from socket import AF_INET, SOCK_STREAM, socket

import log.server_log_config
from common.utils import msg_timestamp, recv_msg, send_msg
from common.variables import (ACCOUNT_NAME, ACTION, ALERT, DEFAULT_ADDR,
                            DEFAULT_PORT, ERROR, FROM, MAX_CONNECTIONS,
                            MESSAGE_TEXT, MSG, PRESENCE, RESPONSE, QUIT,
                            TIME, TO, USER)

from decos import log


# Таймаут для работы функции select()
SELECT_TIMEOUT = 0.1

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
        SERVER_LOGGER.debug('В параметрах запуска скрипта передан порт '
                            'для прослушивания: %d', port)
    else:
        port = DEFAULT_PORT
        SERVER_LOGGER.debug('Назначен порт для прослушивания '
                            'по умолчанию: %d', port)
    SERVER_LOGGER.info('Порт для прослушивания: %d', port)
    return port


@log
def create_server_socket():
    '''Функция создания серверного сокета'''
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
    sock.settimeout(SELECT_TIMEOUT)  # Таймаут для работы функции select()
    return sock


def process_client_msg(msg_from_client_json, msg_list, client_sock, names, connected_clients):
    '''Функция обработки сообщений от клиентов'''

    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {msg_from_client_json}')
    print(f'Разбор сообщения от клиента: {msg_from_client_json}')

    # Если это сообщение PRESENCE, то проверяем,
    # зарегистрирован ли уже такой пользователь
    if ACTION in msg_from_client_json \
            and msg_from_client_json[ACTION] == PRESENCE \
            and TIME in msg_from_client_json \
            and USER in msg_from_client_json:
        # Если ACCOUNT_NAME ещё не зарегистрирован, то регистрируем
        if msg_from_client_json[USER][ACCOUNT_NAME] not in names.keys():
            names[msg_from_client_json[USER][ACCOUNT_NAME]] = client_sock
            msg_to_client_json = {
                RESPONSE: 200,
                ALERT: 'OK',
                TIME: msg_timestamp()
            }
            SERVER_LOGGER.info('Сформировано сообщение клиенту: %s',
                            msg_to_client_json)
            send_msg(client_sock, msg_to_client_json)
        # Если такой ACCOUNT_NAME уже есть, отправляем сообщение об ошибке
        # и закрываем соединение
        else:
            msg_to_client_json = {
                RESPONSE: 409,
                ERROR: 'Такой пользователь уже зарегистрирован',
                TIME: msg_timestamp()
            }
            SERVER_LOGGER.warning('Пользователь уже зарегистрирован. '
                        'Сообщение для отправки клиенту: %s', msg_to_client_json)
            send_msg(client_sock, msg_to_client_json)
            # Закрываем клиентский сокет
            client_sock.close()
            # Удаляем клиентский сокет из общего списка подключённых клиентов
            connected_clients.remove(client_sock)
        return

    # Если это сообщение MSG (сообщение для других клиентов), то добавляем
    # сообщение в список msg_list, ответ не требуется
    elif ACTION in msg_from_client_json \
            and msg_from_client_json[ACTION] == MSG \
            and TIME in msg_from_client_json \
            and TO in msg_from_client_json \
            and FROM in msg_from_client_json \
            and MESSAGE_TEXT in msg_from_client_json:
        msg_list.append(msg_from_client_json)
        SERVER_LOGGER.info(f'Получили сообщение для другого клиента: {msg_from_client_json}')
        return
    # Если это сообщение QUIT (клиент отключается)
    elif ACTION in msg_from_client_json \
            and msg_from_client_json[ACTION] == QUIT \
            and TIME in msg_from_client_json \
            and ACCOUNT_NAME in msg_from_client_json:
        # Удаляем ACCOUNT_NAME из словаря names
        del names[msg_from_client_json[ACCOUNT_NAME]]
        SERVER_LOGGER.info(f'Клиент {client_sock.getpeername()} вышёл по команде QUIT')
        print(f'Клиент {client_sock.getpeername()} вышел по команде QUIT')
        # Закрываем клиентский сокет
        client_sock.close()
        # Удаляем клиентский сокет из общего списка подключённых клиентов
        connected_clients.remove(client_sock)
        return
    # Если запрос неверный, отдаём Bad request
    else:
        msg_to_client_json = {
            RESPONSE: 400,
            ERROR: 'Bad request',
            TIME: msg_timestamp()
        }
        SERVER_LOGGER.warning('Получен неверный запрос от клиента. '
            'Сообщение для отправки клиенту: %s', msg_to_client_json)
        send_msg(client_sock, msg_to_client_json)
        return


@log
def process_p2p_msg(msg_from_client_json, names, listen_socks):
    '''
    Функция обработки и отправки P2P-сообщения
    (от клиента к клиенту)
    '''
    if msg_from_client_json[TO] in names \
            and names[msg_from_client_json[TO]] in listen_socks:
        send_msg(names[msg_from_client_json[TO]], msg_from_client_json)
        SERVER_LOGGER.info(f'Отправлено сообщение {msg_from_client_json} '
            f'от пользователя {msg_from_client_json[FROM]} '
            f'пользователю {msg_from_client_json[TO]}')
    elif msg_from_client_json[TO] in names \
            and names[msg_from_client_json[TO]] not in listen_socks:
        raise ConnectionError
    else:
        print(f'Пользователь {msg_from_client_json[TO]} не зарегистрирован '
            f'на сервере. Отправка сообщения невозможна.')
        SERVER_LOGGER.error(f'Пользователь {msg_from_client_json[TO]} '
            f'не зарегистрирован на сервере. Отправка сообщения невозможна.')



def main():
    
    # Создаём серверный сокет
    server_sock = create_server_socket()

    # Создаём пустой список сокетов подключившихся клиентов
    connected_clients = []

    # Создаём пустой список сообщений
    msg_list = []

    # Создаём пустой словарь с онлайн-пользователями и их сокетами
    names = {}

    while True:
        try:
            client_sock, client_addr = server_sock.accept()
        except OSError:
            pass
        else:
            print(f'Подключился клиент: {client_addr}')
            SERVER_LOGGER.info(f'Подключился клиент: {client_addr}')
            connected_clients.append(client_sock)
        
        # Подготавливаем пустые списки клиентских сокетов для функции select()
        recv_clients = []
        send_clients = []

        # Получаем списки клиентских сокетов, из которых надо почитать и которым надо написать
        try:
            if connected_clients:
                recv_clients, send_clients, err_clients = select.select(connected_clients, connected_clients, [], 0)
        except OSError:
            pass
        
        # Принимаем сообщения от клиентов из списка recv_clients,
        # обрабатываем с помощью функции process_client_msg().
        # Если ошибка, то удаляем клиента из списка recv_clients.
        if recv_clients:
            for client in recv_clients:
                try:
                    msg_from_client_json = recv_msg(client)
                    process_client_msg(msg_from_client_json, msg_list, client, names, connected_clients)
                except Exception as e:
                    print('Возникло исключение:', e)
                    print(f'Клиент {client.getpeername()} отключился')
                    SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключился')
                    # Удаляем клиента из общего списка подключённых
                    connected_clients.remove(client)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщения
        if msg_list and send_clients:
            for msg_to_send in msg_list:
                try:
                    process_p2p_msg(msg_to_send, names, send_clients)
                except Exception as e:
                    print(f'Возникло исключение: {e}')
                    SERVER_LOGGER.info(f'Связь с клиентом {msg_to_send[TO]} '
                        f'была потеряна')
                    print(f'Связь с клиентом {msg_to_send[TO]} была потеряна')
                    # Удаляем клиентский сокет из общего списка подключённых
                    connected_clients.remove(names[msg_to_send[TO]])
                    del names[msg_to_send[TO]]
            # После отправки всех сообщений очищаем список сообщений для отправки
            msg_list.clear()


if __name__ == '__main__':
    main()
