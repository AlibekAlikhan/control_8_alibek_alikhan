from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Comment(models.Model):
    users = models.ForeignKey(to=User, related_name="user", blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey('webapp.Product', related_name='product', on_delete=models.CASCADE, verbose_name="Продукт")
    text_comment = models.CharField(max_length=3000, null=True, verbose_name="Текст Коментария")
    grade = models.IntegerField(verbose_name="Оценка", default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])


    def __str__(self):
        return self.users



