from django import forms
from django.core.validators import RegexValidator, EmailValidator
# custom forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', validators=[RegexValidator('^\w{5,15}$',
    'The username can only contain alphanumeric characters and must be between 5 and 15 characters long')]);
    email = forms.EmailField(label='email', validators=[EmailValidator('Please enter a valid e-mail')]);
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    confirmPassword = forms.CharField(widget=forms.PasswordInput, label='confirmPassword');

class LoginForm(forms.Form):
    email = forms.CharField(label='email', validators=[EmailValidator('Please enter a valid e-mail')])
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    remember = forms.BooleanField(initial=True)