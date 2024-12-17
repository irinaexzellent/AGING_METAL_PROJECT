from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .api import Api
from .constants import *
from .RTable import RTable

def index(request):
    template = 'api/index.html'
    context = {'title': 'Aging metal'}
    return render(request, template, context)

@login_required
def get_table(request, name_table):
    table = RTable(name_table)
    df = table.get_df()
    template = 'api/get_table.html'
    render_context = {
        'df_html': df.to_html(index=False),
        'name_table': name_table,
        'lst_tables': ALL_TABLES,
        'edit_url': 'edit/' + name_table}
    return render(request, template, render_context)

def edit(request, name_table):
    from django.db import IntegrityError
    table = RTable(name_table)
    form = Api.get_form()()
    new = True
    _form = form.get_current_form(name_table, new)()
    template = 'api/edit.html'
    messages = {}
    if request.method == 'POST':
        _form = form.get_current_form(name_table, new)(request.POST)
        if _form.is_valid():
            dict_data = request.POST.dict()
            lst_classes_column = table.get_columns_classes()
            data = {}
            for column in lst_classes_column:
                if lst_classes_column[column][0] in ['ManyToOneRel', 'BigAutoField']:
                    continue
                elif lst_classes_column[column][0] in ['ForeignKey']:
                    obj = getattr(lst_classes_column[column][1], 'objects').get(pk=int(dict_data[column][0]))
                    print('obj', obj)
                    data[column] = obj
                else:
                    data[column] = dict_data[column]
                    pass
            obj = table.model()
            for column in data:
                setattr(obj, column, data[column])
                try:
                    obj.save()
                except IntegrityError as saveException:
                    print(saveException)
            return redirect('api:get_table', name_table=name_table)
    render_context = {
        'name_table': name_table,
        'edit_url': 'edit/' + name_table,
        'form': _form,
        'messages': messages,
    }
    return render(request, template, render_context)