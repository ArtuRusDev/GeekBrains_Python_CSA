"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words_list = ['разработка', 'администрирование', 'protocol', 'standard']


def str_to_bytes(input_list):
    return [item.encode('utf-8') for item in input_list]


def bytes_to_str(input_list):
    return [item.decode('utf-8') for item in input_list]


def print_list(input_list):
    for item in input_list:
        print(item)


words_list_bytes = str_to_bytes(words_list)
print_list(words_list_bytes)

print('_' * 30)

words_list = bytes_to_str(words_list_bytes)
print_list(words_list)
