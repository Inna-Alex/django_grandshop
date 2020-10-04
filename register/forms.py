from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "password"]
