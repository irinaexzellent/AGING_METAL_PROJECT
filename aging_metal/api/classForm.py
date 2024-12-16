from django import forms
from django.forms.models import ModelForm, ModelFormMetaclass

from .RTable import RTable

class Form:
    field_types = {}

    @staticmethod
    def _get_class():
        """ Метод возвращает класс текущей формы """

        class MyForm(ModelForm):
           pass
        return MyForm

    def get_current_form(self, name_table, new=True):

        _table = RTable(name_table)
        fields = {}
        widgets = {}
        column_classes = _table.columns_classes
        for column in column_classes:
            if column_classes[column][0]  == 'CharField':
                fields[column] = forms.CharField(widget=forms.Textarea())
                widgets.update(
                    {column: forms.TextInput(
                        attrs={
                            'class': 'form-control',
                           'placeholder': 'Input text',
                           'type': 'text'}
                        )
                    }
                )
            elif column_classes[column][0] == 'FloatField':
                fields[column] = forms.FloatField()
                widgets.update(
                    {column: forms.NumberInput(
                        attrs={'class': 'form-control',
                               'placeholder': 'Input value',
                               'type': 'number'}
                        )
                    }
                )
            elif column_classes[column][0] == 'DateField':
                fields[column] = forms.DateInput(),
                widgets.update(
                    {column: forms.DateInput(
                        format=('%m/%d/%Y'),
                        attrs={'class': 'form-control',
                               'placeholder': 'Select a date',
                               'type': 'date'}),
                }
                )
            elif column_classes[column][0] == 'ForeignKey':
                queryset_related_model = getattr(column_classes[column][1], 'objects')
                fields[column] = forms.ModelChoiceField(required=False,
                                                        queryset=queryset_related_model,
                                                        empty_label='---------',
                                                        )
                widgets.update(
                    {column: forms.Select(
                        attrs={'class': 'form-control',
                               'placeholder': 'Select a date',}
                    )
                    }
                )
            else:
                pass
        meta_attrs = {
            'model': _table.model,
            'fields': fields,
            'widgets': widgets,
        }
        Meta = type('Meta', (object,), meta_attrs)
        form_class_attrs = {
            'Meta': Meta,
        }
        MyModelForm = ModelFormMetaclass('MyModelForm', (ModelForm,), form_class_attrs)
        return MyModelForm