from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "password",]
