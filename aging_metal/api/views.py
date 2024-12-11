from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .RTable import RTable

def index(request):
    template = 'api/index.html'
    context = {'title': 'Aging metal'}
    return render(request, template, context)

@login_required
def get_table(request, name_table):
    table = RTable(name_table)
    df = table.get_df()
    template = 'api/table.html'
    context = {'df': df.to_html(index=False), 'name_table': name_table}
    return render(request, template, context)