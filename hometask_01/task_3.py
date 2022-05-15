"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

word_1 = 'attribute'
word_2 = 'класс'
word_3 = 'функция'
word_4 = 'type'

word_list = [word_1, word_2, word_3, word_4]


for word in word_list:
    try:
        byteword = bytes(word, 'ascii')
        print(byteword)
    except(UnicodeEncodeError):
        print(f'Текст "{word}" нельзя перевести в байты с кодировкой ASCII')
