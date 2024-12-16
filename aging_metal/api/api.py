from .classForm import Form

class Api:


    @staticmethod
    def get_form():
        """
        Метод возвращает класс для работы с формами
        :return: класс Form
        :rtype class:
        """
        return Form