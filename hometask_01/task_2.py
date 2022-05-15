"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

byteword_1 = b'class'
byteword_2 = b'function'
byteword_3 = b'method'

byteword_list = [byteword_1, byteword_2, byteword_3]

for byteword in byteword_list:
    print(f'Byteword: {byteword}')
    print(f'Type of {byteword}: {type(byteword)}')
    print(f'Length of {byteword}: {len(byteword)}')
    print('==========')


