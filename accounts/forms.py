from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class SignupForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Your email address',
        'class': 'form-control'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-control'
    }))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'username',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-control'
    }))

