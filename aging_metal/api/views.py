from django.shortcuts import render
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
    _form = Api.get_form()()
    new = True
    _form = _form.get_current_form(name_table, new)()
    template = 'api/edit.html'
    render_context = {
        #'df_html': df.to_html(index=False),
        'name_table': name_table,
        'edit_url': 'edit/' + name_table,
        'form': _form,
    }
    return render(request, template, render_context)