from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/<str:name_table>/', views.get_table, name='get_table'),
    path('api/edit/<str:name_table>/', views.edit, name='edit'),
]