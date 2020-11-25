"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

words_list = ['attribute', 'класс', 'функция', 'type']


def str_to_bytes(input_list):
    for item in input_list:
        try:
            print(bytes(item, 'ascii'))
        except UnicodeEncodeError:
            print(f'Слово "{item}" нельзя закодировать в ASCII')


str_to_bytes(words_list)
