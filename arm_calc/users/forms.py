from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        required=True,
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=True,
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
