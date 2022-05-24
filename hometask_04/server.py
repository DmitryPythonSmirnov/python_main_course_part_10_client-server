'''
Сервер
'''

# TODO Сделать перехват Ctrl+C для остановки сервера

from socket import socket, AF_INET, SOCK_STREAM
import sys

from common.variables import DEFAULT_ADDR, DEFAULT_PORT, ACTION, ALERT, ERROR, \
    RESPONSE, TIME, PRESENCE, MAX_CONNECTIONS

from common.utils import recv_msg, send_msg, msg_timestamp


def get_addr():
    '''
    Функция получает адрес сервера из командной строки
    или возращает дефолтное значение'''
    if '-a' in sys.argv:
        a_key_index = sys.argv.index('-a')
        addr_index = a_key_index + 1
        addr = sys.argv[addr_index]
    else:
        addr = DEFAULT_ADDR
    return addr

def get_port():
    '''
    Функция получает порт из командной строки
    или возращает дефолтное значение'''
    if '-p' in sys.argv:
        p_key_index = sys.argv.index('-p')
        port_index = p_key_index + 1
        port = int(sys.argv[port_index])
    else:
        port = DEFAULT_PORT
    return port


def generate_msg_to_client(msg_from_client_json):
    msg_to_client_json = {}
    if ACTION in msg_from_client_json and msg_from_client_json['action'] == PRESENCE:
        msg_to_client_json[RESPONSE] = 200
        msg_to_client_json[ALERT] = 'OK'
    else:
        msg_to_client_json[RESPONSE] = 400
        msg_to_client_json[ERROR] = 'Bad request'
    
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
    sock.listen(MAX_CONNECTIONS)

    while True:
        client_connection, client_addr = sock.accept()
        msg_from_client_json = recv_msg(client_connection)
        print(f'Получено от клиента {client_addr}: {msg_from_client_json}')
        msg_to_client_json =  generate_msg_to_client(msg_from_client_json)
        send_msg(client_connection, msg_to_client_json)
        print(f'Отправлено клиенту {client_addr}: {msg_to_client_json}')

        if client_connection:
            client_connection.close()


if __name__ == '__main__':
    main()
