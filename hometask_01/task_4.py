"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

word_1 = 'разработка'
word_2 = 'администрирование'
word_3 = 'protocol'
word_4 = 'standard'

word_list = [word_1, word_2, word_3, word_4]
byteword_list = []

print('Преобразование из строк в байты (кодировка UTF-8)')
for word in word_list:
    byteword = word.encode('utf-8')
    print(f"{word}: {byteword}")
    byteword_list.append(byteword)

print('==================================================')

print('Преобразование из байт в строку (кодировка UTF-8)')
for byteword in byteword_list:
    print(byteword.decode('utf-8'))
