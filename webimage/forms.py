from django import forms
from django.core.validators import RegexValidator, EmailValidator


# custom forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', validators=[RegexValidator('^\w{5,15}$',
                                                                            'The username can only contain alphanumeric characters and must be between 5 and 15 characters long (Aplhanumeric or underscore)')],
                               widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True, error_messages={'required': 'First name field is required.'})
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True, error_messages={'required': 'Last name field is required.'})
    email = forms.EmailField(label='Email', validators=[EmailValidator(
        'Please enter a valid e-mail')], widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='password',
                               validators=[
                                   RegexValidator(
                                       '[a-zA-Z]+', 'The password must contain one or more letters'),
                                   RegexValidator(
                                       '[0-9]+', 'The password must contain one or more digits'),
                                   RegexValidator(
                                       '[!@#$%^&_]+',
                                       'The password must contain at least one special symbol "!@#$%^&_"'),
                                   RegexValidator('^.{5,20}$', 'The password must be 5-15 characters long')],
                               required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Password Confirmation', required=True)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='New password',
                               validators=[
                                   RegexValidator(
                                       '[a-zA-Z]+', 'The password must contain one or more letters'),
                                   RegexValidator(
                                       '[0-9]+', 'The password must contain one or more digits'),
                                   RegexValidator(
                                       '[!@#$%^&_]+',
                                       'The password must contain at least one special symbol "!@#$%^&_"'),
                                   RegexValidator('^.{5,20}$', 'The password must be 5-15 characters long')],
                               required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='New password Confirmation', required=False)


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', validators=[EmailValidator(
        'Please enter a valid e-mail')], widget=forms.TextInput(attrs={'class': "form-control", "type": "email"}),
                            required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Password', required=True)
    remember = forms.BooleanField(label='Remember Me', initial=True, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False)


class AlbumForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True, error_messages={'required': 'Album name is required.'})
    private = forms.BooleanField(label='Private', initial=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)


class ImagesForm(forms.Form):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control-file'}))
