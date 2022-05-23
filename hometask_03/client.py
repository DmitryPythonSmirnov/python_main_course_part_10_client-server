'''
Программа-клиент.
Запускать скрипт из командной строки с параметрами: python client.py 127.0.0.1 7777.
Скрипт запрашивает, какое сообщение отправить серверу.
Для выхода - q.
'''

# TODO Сделать выбор отправляемого сообщения - запрос в бесконечном цикле, выход по q

from socket import socket, AF_INET, SOCK_STREAM
import sys

from common.variables import AUTHENTICATE, PASSWORD, DEFAULT_ADDR, DEFAULT_PORT, \
    ACCOUNT_NAME, ACTION, USER, TIME, PRESENCE

from common.utils import recv_msg, send_msg, msg_timestamp


def get_addr():
    '''
    Функция получает адрес сервера из командной строки
    или возращает дефолтное значение'''
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = DEFAULT_ADDR
    return addr

def get_port():
    '''
    Функция получает порт из командной строки
    или возращает дефолтное значение'''
    try:
        port = int(sys.argv[2])
    except (IndexError, ValueError):
        port = DEFAULT_PORT
    return port


def msg_presence(account_name='Guest'):
    '''Функция отправки сообщения PRESENCE'''
    msg_to_server_json = {
        ACTION: PRESENCE,
        TIME: msg_timestamp(),
        USER: {
            ACCOUNT_NAME: account_name,
        }
    }
    return msg_to_server_json


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
    
    # Отправляем сообщение PRESENCE
    msg_to_server = msg_presence()
    send_msg(sock, msg_to_server)
    print(f'Отправлено сообщение {msg_to_server}')

    msg_from_server = recv_msg(sock)
    print(f'Получено сообщение: {msg_from_server}')

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


    # Отправляем сообщение AUTHENTICATE - для проверки получения ошибки
    msg_to_server = msg_auth()
    send_msg(sock, msg_to_server)
    print(f'Отправлено сообщение {msg_to_server}')
    
    msg_from_server = recv_msg(sock)
    print(f'Получено сообщение: {msg_from_server}')
    
    if sock:
        sock.close()


if __name__ == '__main__':
    main()
