'''
Файл для понимания работы модуля traceback
'''

import traceback

def func1():
    # print(f'func1 вызвана из {traceback.format_stack()[0].strip().split()[-1]}')
    print(f'func1 вызвана из {traceback.format_stack()[-2].split()[-2]}')
    # for tb in traceback.format_stack():
    #     print(tb)


def func2():
    func1()
    # print(f'func2 вызвана из {traceback.format_stack()[0].strip().split()[-1]}')
    print(f'func2 вызвана из {traceback.format_stack()[-2].split()[-2]}')


def func3():
    func1()
    func2()
    print(f'func3 вызвана из {traceback.format_stack()[-2].split()[-2]}')


def main():
    func1()
    print('=====')
    func2()
    print('=====')
    func3()


main()
