'''
Программа-клиент.
Можно запускать скрипт из командной строки с параметрами:

python client.py 127.0.0.1 7777 -m (send|listen)

Либо адрес порт будут по умолчанию, а режим работы клиента
будет запрошен у пользователя.
'''

import logging
import sys
import threading
import time
from socket import AF_INET, SOCK_STREAM, socket

import log.client_log_config
from common.utils import msg_timestamp, recv_msg, send_msg
from common.variables import (ACCOUNT_NAME, ACTION, AUTHENTICATE, DEFAULT_ADDR,
                            DEFAULT_PORT, FROM, MESSAGE_TEXT, MSG, PASSWORD,
                            PRESENCE, QUIT, TIME, TO, USER)

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
def msg_presence(account_name='Guest'):
    '''Функция создания сообщения PRESENCE'''
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
    '''Функция создания сообщения AUTHENTICATE'''
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
def msg_quit(account_name):
    '''Функция создания сообщения QUIT'''
    msg_to_server_json = {
        ACTION: QUIT,
        TIME: msg_timestamp(),
        ACCOUNT_NAME: account_name,
    }
    CLIENT_LOGGER.info('Сообщение для отправки на сервер: %s', msg_to_server_json)
    return msg_to_server_json


@log
def create_message(sock, account_name='Guest'):
    '''Функция запрашивает сообщение для отправки и отправляет его'''
    to_user = input('Введите получателя: ')
    input_msg = input('Введите сообщение для отправки: ')
    msg_to_send_json = {
        ACTION: MSG,
        TIME: msg_timestamp(),
        FROM: account_name,
        TO: to_user,
        MESSAGE_TEXT: input_msg
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение для отправки: {msg_to_send_json}')
    try:
        send_msg(sock, msg_to_send_json)
        CLIENT_LOGGER.info(f'Отправлено сообщение {msg_to_send_json}')
    except:
        CLIENT_LOGGER.critical(f'Не удалось отправить сообщение {msg_to_send_json}')
        sys.exit(1)


@log
def print_help():
    """Функция, выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def user_interactive(sock, username):
    '''
    Функция взаимодействия с пользователем,
    запрашивает команды, отправляет сообщения
    '''
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_msg(sock, msg_quit(username))
            print('Завершение соединения')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Неверная команда. Попробуйте снова. help - вывести поддерживаемые команды')



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


@log
def process_p2p_msg(sock, my_account_name):
    '''
    Функция обрабатывает P2P-сообщения, полученные от сервера
    (сообщения были отправлены другими клиентами клиенту my_account_name
    через сервер)
    '''
    while True:
        try:
            message = recv_msg(sock)
            if ACTION in message and message[ACTION] == MSG \
                    and TIME in message \
                    and FROM in message \
                    and TO in message \
                    and message[TO] == my_account_name \
                    and MESSAGE_TEXT in message:
                print(f'\nПолучено сообщение от пользователя {message[FROM]}: '
                    f'{message[MESSAGE_TEXT]}')
                    # f'Введите команду: ')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[FROM]}: '
                    f'{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError):
            CLIENT_LOGGER.critical('Потеряно соединение с сервером')
            break
        except Exception as e:
            CLIENT_LOGGER.critical(f'Произошло исключение: {e}')
            break


def main():

    # Получаем адрес сервера и порт для подключения,
    # а также режим работы клиента из параметров запуска скрипта
    # или дефолтные значения (режим работы клиента в этом случае
    # нужно ввести вручную)
    serv_addr = get_addr()
    serv_port = get_port()
    
    print(f'Запущен клиент с параметрами: адрес сервера {serv_addr}, '
        f'порт сервера {serv_port}, режим двунаправленный')
    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: адрес сервера {serv_addr}, '
        f'порт сервера {serv_port}, режим двунаправленный')
    
    # Запрашиваем имя пользователя
    client_name = input('Введите ваш аккаунт: ')
    
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
    else:
        # Если подключение успешно, сначала отправляем сообщение PRESENCE
        send_msg(sock, msg_presence(client_name))

        # Затем запускаем приём сообщений в отдельном потоке
        receiver = threading.Thread(target=process_p2p_msg, args=(sock, client_name))
        receiver.daemon = True
        receiver.start()
    
        # Затем запускаем взаимодействие с пользователем в отдельном потоке
        user_interface = threading.Thread(target=user_interactive, args=(sock, client_name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.info('Запущены потоки на приём сообщений и взаимодействие с пользователем')

        # Watchdog основной цикл, если один из потоков завершён,
        # то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках,
        # достаточно просто завершить цикл.
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
