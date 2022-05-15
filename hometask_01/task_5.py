"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import subprocess
import chardet

YANDEX_ARGS = ['ping', 'yandex.ru']
YUOTUBE_ARGS = ['ping', 'youtube.com']


def myping(args_list):
    ping_subprocess = subprocess.Popen(args_list, stdout=subprocess.PIPE)
    for line in ping_subprocess.stdout:
        detect_result = chardet.detect(line)
        print(line.decode(detect_result['encoding']), end='')

    print(f"""
    Результат автоматического детектирования последней строки:
    Предполагаемая кодировка: {detect_result['encoding']}
    Уровень уверенности: {detect_result['confidence']}
    Предполагаемый язык: {detect_result['language']}
    """)

myping(YANDEX_ARGS)
myping(YUOTUBE_ARGS)