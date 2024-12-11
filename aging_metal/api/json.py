import os
import json

from django.conf import settings

class JsonData:

    _tables_data_file_ = os.path.join(settings.BASE_DIR, 'data', 'tables.json')
    dv = "DEFAULTS_VALUES_FOR_LABEL"

    _tables_data_ = {}

    def __new__(cls):
        """
        The method checks that there is only one instance of the JsonData class
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(JsonData, cls).__new__(cls)
            cls.instance.get_data()
        return cls.instance

    def get_data(self):
        """
        The method reads data from a file '_tables_data_file_'
        """
        if os.path.exists(self._tables_data_file_):
            with open(self._tables_data_file_, "r", encoding="utf-8") as f:
                try:
                    self._tables_data_ = json.load(f)
                except Exception as e:
                    pass

    def get_key(self, *keys):
        """
        The method gets the value by keys

        :param list/str keys: key sequence
        :return: data
        """
        data = self._tables_data_
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None
        return data

    def set_key(self, *keys, value):
        """
        The method sets the value 'value' for a sequence of keys 'keys'

        :param list/str keys: key sequence
        :param value: key sequence
        """
        data = self._tables_data_
        for i in range(0, len(keys)):
            if keys[i] not in data:
                data[keys[i]] = {} if i < len(keys) - 1 else value
            data = data[keys[i]]

    def get_default_labels(self):
        """
        The method gets a list of default labels

        :return: defaults
        :rtype: list
        """
        defaults = self.get_key(self.dv)
        if not isinstance(defaults, list):
            defaults = []
        return defaults
