from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, BaseValidator

from webapp.models import Product

from webapp.models import Comment


class CustomLenValidator(BaseValidator):
    def __init__(self, limit_value):
        message = "Максимум можно ввести %(limit_value)s символов, а вы ввели %(show_value)s"
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return value > limit_value

    def clean(self, value):
        return len(value)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("category", "name", "text", "image_url")
        labels = {
            'category': 'Категория',
            'name': 'Имя',
            'text': 'Текст',
            'image_url': 'Фото',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text_comment", "grade")
        labels = {
            'text_comment': 'Коментарий',
            'grade': 'Оценка'
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Найти')



