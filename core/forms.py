from django import forms

from core.utils.forms import SimpleRequestPostForm


class LoginRequestForm(SimpleRequestPostForm):
    username = forms.CharField(label="Usuário", max_length=100)
    password = forms.CharField(label="Senha", max_length=100, widget=forms.PasswordInput())
