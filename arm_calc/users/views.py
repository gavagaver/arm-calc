from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import CreationForm


class SignUp(CreateView):
    """
    A view for signing up a new user.
    """
    form_class = CreationForm
    success_url = reverse_lazy('calc:landing')
    template_name = 'users/signup.html'


class PasswordChangeDone(TemplateView):
    """
    A view for displaying a message after a user
    has successfully changed their password.
    """
    template_name = 'users/password_change'


class PrivacyPolicyView(TemplateView):
    """
    A view for displaying the site's privacy policy.
    """
    template_name = 'users/privacy-policy.html'
