"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import csv


file_1 = 'info_1.txt'
file_2 = 'info_2.txt'
file_3 = 'info_3.txt'
FILE_LIST = [file_1, file_2, file_3]

header_os_prod = 'Изготовитель системы'
header_os_name = 'Название ОС'
header_os_code = 'Код продукта'
header_os_type = 'Тип системы'
CSV_HEADERS = [header_os_prod, header_os_name, header_os_code, header_os_type]

# Итоговый файл для сохранения результата
CSV_REPORT_FILE = 'my_report.csv'


def get_data(lst_of_files):
    '''Парсинг файлов. Функция возвращает список списков'''
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for filename in lst_of_files:
        with open(filename, encoding='utf-8') as f:
            # Так как файлы небольшие, сразу преобразуем весь файл
            # в список строк, после этого проверяем каждую строку
            for line in f.readlines():
                for header in CSV_HEADERS:
                    if header in line:
                        # Забираем значение - убираем пробелы после header и знака ":"
                        value = line[len(header) + 1:].strip()
                        # Добавляем значение в соответствующий список
                        if header == header_os_prod:
                            os_prod_list.append(value)
                        elif header == header_os_name:
                            os_name_list.append(value)
                        elif header == header_os_code:
                            os_code_list.append(value)
                        elif header == header_os_type:
                            os_type_list.append(value)
            
            # Формируем итоговый список списков
            main_data = [CSV_HEADERS]
            for i in range(len(os_prod_list)):
                temp_list = [i + 1]
                temp_list.append(os_prod_list[i])
                temp_list.append(os_name_list[i])
                temp_list.append(os_code_list[i])
                temp_list.append(os_type_list[i])
                main_data.append(temp_list)

    return main_data


def write_to_csv(filename):
    '''Запись результатов парсинга в файл'''
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(get_data(FILE_LIST))


# Вызов основной функции
write_to_csv(CSV_REPORT_FILE)
