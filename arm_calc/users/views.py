from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('calc:landing')
    template_name = 'users/signup.html'


class PasswordChangeDone(TemplateView):
    template_name = 'users/password_change'


class PrivacyPolicyView(TemplateView):
    template_name = 'users/privacy-policy.html'
