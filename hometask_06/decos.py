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
        LOGGER.debug(f'Вызвана функция {func.__name__} '
                    f'с параметрами: args={args}, kwargs={kwargs}, '
                    # f'''из модуля {traceback.format_stack()[0].strip().split()[1].strip(',"').split('/')[-1]}, '''
                    f'''из модуля {traceback.format_stack()[0].split()[1].strip(',"').split('/')[-1]}, '''
                    # f'из функции {traceback.format_stack()[-2].split()[-2]}')
                    f'из функции {traceback.format_stack()[0].strip().split()[-1]}')
        return func(*args, **kwargs)
    return wrapper
