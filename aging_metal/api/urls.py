from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/<str:name_table>/', views.get_table, name='get_table'),
    path('api/<str:name_table>/edit', views.edit, name='add'),
    path('api/<str:name_table>/edit/<int:pk>', views.edit, name='edit'),
]