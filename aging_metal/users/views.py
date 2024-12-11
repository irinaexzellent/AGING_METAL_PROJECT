from django.views.generic import CreateView, UpdateView

from django.contrib.auth.views import LoginView

from django.urls import reverse, reverse_lazy

from .forms import CreationForm

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('api:index')
    template_name = 'users/signup.html'

class MyLoginView(LoginView):

    def get_success_url(self):
        return reverse('api:index')