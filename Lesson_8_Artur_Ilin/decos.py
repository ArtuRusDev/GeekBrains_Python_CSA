import sys
import logging.handlers
import inspect

if 'client' in sys.argv[0]:
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')


def log(func):
    def wrapper(*args, **kwargs):
        func_res = func(*args, **kwargs)
        LOGGER.debug(
            f'Вызвана функция {func.__name__} с параметрами {args} и {kwargs}. Модуль функции: {func.__module__}. Вызов из функции {inspect.stack()[1][3]}',
            stacklevel=2)
        return func_res

    return wrapper


class Log:
    def __call__(self, func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            func_res = func(*args, **kwargs)
            LOGGER.debug(
                f'Вызвана функция {func.__name__} с параметрами {args} и {kwargs}. Модуль функции: {func.__module__}. Вызов из функции {inspect.stack()[1][3]}',
                stacklevel=2)
            return func_res

        return wrapper
