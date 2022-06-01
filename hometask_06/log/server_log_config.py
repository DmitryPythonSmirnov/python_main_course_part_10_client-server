import logging
import logging.handlers
import os


# Выносим уровень логирования в константу
LOGGING_LEVEL = logging.DEBUG

# Вычисляем путь для файла 'server.log', так как он всегда
# должен находться в каталоге 'log', не зависимо от того,
# где запускается логгер, который в него пишет
filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)
server_log_path = os.path.join(dirpath, 'server.log')


# Создаём логгер
server_logger = logging.getLogger('server_logger')

# Создаём обработчик - логирование в файл с ротацией файла в полночь
fh = logging.handlers.TimedRotatingFileHandler(server_log_path, when='midnight', interval=1, encoding='utf-8')

# Устанавливаем формат сообщений
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)-10s %(message)s')

# Назначаем формат обработчику
fh.setFormatter(formatter)

# Устанавливаем уровень сообщений для обработчика
fh.setLevel(LOGGING_LEVEL)

# Подключаем обработчик к логгеру
server_logger.addHandler(fh)

# Устанавливаем уровень сообщений для логгера
server_logger.setLevel(LOGGING_LEVEL)

# Проверка
if __name__ == '__main__':
    server_logger.debug('Тестовое сообщение уровня DEBUG')
    server_logger.info('Тестовое сообщение уровня INFO')
    server_logger.warning('Тестовое сообщение уровня WARNING')
    server_logger.error('Тестовое сообщение уровня ERROR')
    server_logger.critical('Тестовое сообщение уровня CRITICAL')
