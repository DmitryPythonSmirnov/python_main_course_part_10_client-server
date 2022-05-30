import logging
import os

# Выносим уровень логирования в константу
LOGGING_LEVEL = logging.DEBUG

# Вычисляем путь для файла 'client.log', так как он всегда
# должен находться в каталоге 'log', на зависимо от того,
# где запускается логгер, который в него пишет
filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)
client_log_path = os.path.join(dirpath, 'client.log')


# Создаём логгер
client_logger = logging.getLogger('client_logger')

# Создаём обработчик - логирование в файл
fh = logging.FileHandler(client_log_path, encoding='utf-8')

# Устанавливаем формат сообщений
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)-10s %(message)s')

# Назначаем формат обработчику
fh.setFormatter(formatter)

# Устанавливаем уровень сообщений для обработчика
fh.setLevel(LOGGING_LEVEL)

# Подключаем обработчик к логгеру
client_logger.addHandler(fh)

# Устанавливаем уровень сообщений для логгера
client_logger.setLevel(LOGGING_LEVEL)

# Проверка
if __name__ == '__main__':
    client_logger.debug('Тестовое сообщение уровня DEBUG')
    client_logger.info('Тестовое сообщение уровня INFO')
    client_logger.warning('Тестовое сообщение уровня WARNING')
    client_logger.error('Тестовое сообщение уровня ERROR')
    client_logger.critical('Тестовое сообщение уровня CRITICAL')
