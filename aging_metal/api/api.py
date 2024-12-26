from .classForm import Form

class Api:


    @staticmethod
    def get_form():
        """
        The method returns a class for working with forms.
        :return: class Form
        :rtype class:
        """
        return Form

    @staticmethod
    def get_r_table_cls():
        """
        Метод возвращает класс для работы с таблицами - RdbTable
        :return: класс RdbTable
        :rtype class:
        """
        from .RTable import RTable
        return RTable