from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(
                                   attrs={
                                       "id": "username",
                                       "class": "form-control",
                                       "placeholder": 'Username',
                                       'required': True,
                                       "autofocus": "autofocus",
                                   }
                               ))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(
                                   attrs={
                                       "id": "password",
                                       "class": "form-control",
                                       "placeholder": 'Password',
                                       'required': True,
                                   }
                               ))
