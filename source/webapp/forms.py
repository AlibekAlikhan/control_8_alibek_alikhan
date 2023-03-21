from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, BaseValidator

from webapp.models import Task

from webapp.models import Project


class CustomLenValidator(BaseValidator):
    def __init__(self, limit_value):
        message = "Максимум можно ввести %(limit_value)s символов, а вы ввели %(show_value)s"
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return value > limit_value

    def clean(self, value):
        return len(value)


class ArticleForm(forms.ModelForm):
    text = forms.CharField(
        validators=(MinLengthValidator(limit_value=2, message='Введите больше 2 символов'), CustomLenValidator(30)))
    detail_text = forms.CharField(
        validators=(MinLengthValidator(limit_value=1, message='Введите больше 1 символов'), CustomLenValidator(100)))

    class Meta:
        model = Task
        fields = ("status", "teg", "text", "detail_text", "project")
        labels = {
            'status': 'Статус',
            'text': 'Текст',
            'teg': 'Тег',
            'project': 'Проект',
            'detail_text': 'Детальный текст',
        }


class ProjectForm(forms.ModelForm):
    start_at = forms.DateField(label='Время начала', widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
                               required=False)
    end_at = forms.DateField(label='Время конца', widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
                               required=False)
    class Meta:
        model = Project
        fields = ("start_at", "end_at", "name", "text_project", "users")
        labels = {
            'start_at': 'Время начала',
            'end_at': 'Время конца',
            'name': 'Название',
            'text_project': 'Текст',
            "users": "Пользователь"
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Найти')
