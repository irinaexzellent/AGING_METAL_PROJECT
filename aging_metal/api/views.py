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
    df = table.get_df(request.path_info)
    template = 'api/get_table.html'
    render_context = {
        'df_html': df.to_html(escape=False, index=False),
        'name_table': name_table,
        'lst_tables': ALL_TABLES,
        'edit_url': 'edit/' + name_table}
    return render(request, template, render_context)

def edit(request, name_table, pk=''):
    from django.db import IntegrityError
    table = RTable(name_table)
    form = Api.get_form()()
    new = True
    _form = form.get_current_form(name_table, new)()
    template = 'api/edit.html'
    messages = {}
    obj_for_edit = None
    if pk != '':
        new = False
        obj_for_edit = getattr(table.model, 'objects').get(pk=pk)
        _context_t = {clm: getattr(obj_for_edit, clm) for clm in table.get_main_name_columns()}
        for clm in _context_t:
            _form.initial[clm] = _context_t[clm]
    if request.method == 'POST':
        if obj_for_edit is not None:
            _form = form.get_current_form(name_table, new)(request.POST, instance=obj_for_edit)
            obj = obj_for_edit
        else:
            _form = form.get_current_form(name_table, new)(request.POST)
            obj = table.model()
        if _form.is_valid():
            dict_data = request.POST.dict()
            if _form.is_valid():
                lst_classes_column = table.get_columns_classes()
                main_columns = table.get_main_name_columns()
                print('lst_classes_column', lst_classes_column)
                data = {}
                for column in lst_classes_column:
                    if lst_classes_column[column][0] in ['ManyToOneRel', 'BigAutoField']:
                        continue
                    elif lst_classes_column[column][0] in ['ForeignKey']:
                        obj_related_table = getattr(lst_classes_column[column][1], 'objects').get(pk=int(dict_data[column][0]))
                        data[column] = obj_related_table
                    else:
                        data[column] = dict_data[column]
                        pass
                for column in data:
                    setattr(obj, column, data[column])
                try:
                    if new is True:
                        obj.save()
                    else:
                        obj.save(update_fields=main_columns)
                except IntegrityError as saveException:
                    print('saveException', saveException)
                return redirect('api:get_table', name_table=name_table)
    render_context = {
        'name_table': name_table,
        'edit_url': 'edit/' + name_table,
        'form': _form,
        'messages': messages,
    }
    return render(request, template, render_context)