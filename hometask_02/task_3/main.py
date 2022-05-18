"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml
from yaml import Loader


RESULT_FILE = 'myfile.yaml'

# Данные для записи в файл
DATA = {
    'Ω': [1, 'два', 3],
    'Ψ': 123,
    'Σ': {'val1': 'пять', 'val2': 10}
}

# Запись в файл
with open(RESULT_FILE, 'w', encoding='utf-8') as f:
    yaml.dump(DATA, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

# Чтение из файла
with open(RESULT_FILE, encoding='utf-8') as f:
    content = yaml.load(f, Loader=Loader)
    print(content)

print(DATA == content)
