class IncorrectDataRecivedError(Exception):
    def __str__(self):
        return 'Получено некорректное сообщение'


class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class NonDictInputError(Exception):
    def __str__(self):
        return 'Функция принимает только словарь'


class ReqFieldMissingError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В полученном словаре нет необходимого поля {self.missing_field}.'
