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

words_list = [b'class', b'function', b'method']


def get_types(words):
    for word in words:
        print(f'{word}({len(word)}) - {type(word)}')


get_types(words_list)
