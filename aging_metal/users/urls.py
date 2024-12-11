from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView

from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',
         views.SignUp.as_view(), name='signup'
         ),
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'), name='logout'
         ),
    path('login/',
         views.MyLoginView.as_view(template_name='users/login.html', success_url = reverse_lazy('api:index')), name='login'
         ),
    path('password_change/', PasswordChangeView.as_view(
        template_name='users/password_change_form.html'), name='password_change'
         ),
    path('password_change/done/', PasswordChangeDoneView.as_view(
         template_name='users/password_change_done.html'), name='password_change_done'),

    # Доработать
    path('password_reset/', PasswordResetView.as_view(
         template_name='users/password_reset_form.html'),
         name='password_reset'),

    # Сообщение об отправке ссылки для восстановления пароля
    path('password_reset/done/', PasswordResetDoneView.as_view(
         template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    # Вход по ссылке для восстановления пароля
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
         template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # Сообщение об успешном восстановлении пароля
    path('reset/done/', PasswordResetCompleteView.as_view(
         template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]