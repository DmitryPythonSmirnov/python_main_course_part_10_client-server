"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "принтер", (возможные проблемы с кирилицей)
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""

import json


RESULT_FILE = 'orders.json'


def write_order_to_json(item, quantity, price, buyer, date):
    '''Запись заказа в JSON-файл'''
    # Считываем информацию из файла
    with open(RESULT_FILE, encoding='utf-8') as f:
        content = json.load(f)
    
    # Формируем новый контент для записи в файл
    # (добавляем новый заказ)
    data = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }
    content['orders'].append(data)

    # Записываем контент в файл
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


# Вызов основной функции
write_order_to_json("сканер", "5", "3300", "Симонов А.В.", "03.11.2021")
write_order_to_json("принтер", "10", "4560", "Белова Т.А.", "25.04.2020")
write_order_to_json("стол компьютерный", "7", "12000", "Захаров К.В.", "15.05.2020")
