from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile
from django.urls import reverse
from django.views.generic import UpdateView


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Логин")
    password = forms.CharField(required=True, label="Пароль", widget=forms.PasswordInput)


class CustomUserCreation(forms.ModelForm):
    password = forms.CharField(label="Пароль", strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", strip=False, required=True,
                                       widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.groups.add('user')
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class UserAdd(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='User')


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Почта'}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'birth_date')




