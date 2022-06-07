import logging
import sys
import traceback

import log.client_log_config
import log.server_log_config


if sys.argv[0].find('server.py') >= 0:
    # Получаем серверный логгер из 'log.server_log_config'
    LOGGER = logging.getLogger('server_logger')
elif sys.argv[0].find('client.py') >= 0:
    # Получаем клиентский логгер из 'log.client_log_config'
    LOGGER = logging.getLogger('client_logger')
else:
    print('Вы запустили не тот файл')

def log(func):
    '''Декоратор для логирования'''
    def wrapper(*args, **kwargs):
        module_name = traceback.format_stack()[0].split()[1].strip(',"').split('/')[-1].split('\\')[-1]
        func_name = traceback.format_stack()[0].strip().split()[-1]
        LOGGER.debug(f'Вызвана функция {func.__name__} '
                    f'с параметрами: args={args}, kwargs={kwargs}, '
                    f'из модуля {module_name}, '
                    f'из функции {func_name}')
        return func(*args, **kwargs)
    return wrapper
