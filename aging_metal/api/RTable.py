import pandas as pd

from django.apps import apps

from .json import JsonData

class RTable:
    """
    Class for working with a database table
    """

    name_table = None

    _types = {}


    def __init__(self, name_table=""):
        self.name_table = name_table
        self.model = next((m for m in apps.get_models() if m._meta.db_table == name_table), None)
        self.object = getattr(self.model, 'objects')
        self.json_data = JsonData()
        self.columns_classes = self.get_columns_classes()

    def get_columns_classes(self, key=None):
        parameters_fields = getattr(self.model, '_meta').get_fields()
        data_columns = {}
        for _field in parameters_fields:
            if 'related_model' in _field.__dict__:
                d = (type(_field).__name__, _field.__dict__['related_model'])
            else:
                d = (type(_field).__name__, None)

            data_columns[_field.name] = d
        return data_columns

    def get_db_type(self, key=None):
        """
        Метод возвращает название типа данных для конкретной бд

        :param str key: название типа данных
        :return: тип данных для бд / если key=None, то возвращаем все типы
        """
        _type = None
        if key is None:
            return self._db_types
        elif key in self._db_types:
            _type = self._db_types[key]
        return _type

    def get_name_fields(self):
        total_records = self.object.all()
        return [item.name for item in total_records.model._meta.concrete_fields]

    def get_df(self):
        total_records = self.object.all()
        fields = self.get_name_fields()
        dict_fk_fields_and_related_tables = {}
        for field in fields:
            d = getattr(self.model, field)
            a = d.field.__dict__
            if 'related_fields' in a:
                dict_fk_fields_and_related_tables[field] = d.field.related_model._meta.db_table

        df = pd.DataFrame(
            total_records.values(*fields),
            columns=fields
        )

        dict_unique_values_for_fk_fields = {}
        for field, related_table in dict_fk_fields_and_related_tables.items():
            json_data = JsonData()
            label_related_table = json_data.get_key(related_table)
            model = next((m for m in apps.get_models() if m._meta.db_table == related_table), None)
            object_related_table = getattr(model, 'objects')
            lst_values_current_fk_field = list(df[field].unique())
            d = {}
            for value in lst_values_current_fk_field:
                query_set = object_related_table.filter(pk=value)
                model_to_dict=[model for model in query_set.values()]
                d[value] = model_to_dict[0][label_related_table['label']]
            dict_unique_values_for_fk_fields[field] = d
        for field in dict_unique_values_for_fk_fields:
            for key in dict_unique_values_for_fk_fields[field]:
                f = lambda x: dict_unique_values_for_fk_fields[field][key] if x == key else x
                df[field] = df[field].map(f)
        return df