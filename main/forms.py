from django import forms
from . import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True)
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        required=True,
        min_length=8
    )

    email.widget.attrs.update({'class': 'email', 'placeholder': 'E-mail', 'autocomplete': 'false'})
    password.widget.attrs.update({'class': 'password', 'placeholder': 'Пароль'})


    def clean_email(self):
        email_data = self.cleaned_data['email']
        user_list = User.objects.all()
        exist = False
        for user in user_list:
            if user.email == email_data:
                exist = True
                break
        if not exist:
            raise ValidationError('Неверная почта')
        return email_data

    def clean_password(self):
        password_data = self.cleaned_data['password']
        if len(password_data) < 8:
            raise ValidationError('Пароль должен содержать не меньше 8 символов')
        return password_data

class SignupForm(forms.Form):
    name = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=8)
    re_password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=8)

    email.widget.attrs.update({'class': 'email', 'placeholder': 'E-mail'})
    password.widget.attrs.update({'class': 'password', 'placeholder': 'Пароль'})
    name.widget.attrs.update({'class': 'name', 'placeholder': 'Имя'})
    surname.widget.attrs.update({'class': 'surname', 'placeholder': 'Фамилия'})
    re_password.widget.attrs.update({'class': 're_password', 'placeholder': 'Повторите пароль'})
    username.widget.attrs.update({'class': 'username', 'placeholder': 'Ник'})

    def clean_email(self):
        email_data = self.cleaned_data['email']
        user_list = User.objects.all()
        for user in user_list:
            if user.email == email_data:
                raise ValidationError('Почта занята')
        return email_data

    def clean_username(self):
        username_data = self.cleaned_data['username']
        user_list = User.objects.all()
        for user in user_list:
            if user.username == username_data:
                raise ValidationError('Этот ник уже занят')
        return username_data

    def clean_password(self):
        password_data = self.cleaned_data['password']
        if len(password_data) < 8:
            raise ValidationError('Пароль должен содержать не меньше 8 символов')
        return password_data

    def clean_re_password(self):
        re_password_data = self.cleaned_data['re_password']
        password = self.cleaned_data['password']
        if re_password_data != password:
            raise ValidationError('Пароли не совпадают')
        return re_password_data

class ReviewForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    rates = [(mark, mark) for mark in range(1, 11)]
    rate = forms.ChoiceField(widget=forms.Select, choices=rates)

    comment.widget.attrs.update({'class': 'new_comment', 'autofocus': True})