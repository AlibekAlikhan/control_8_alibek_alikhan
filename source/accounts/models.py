from django.contrib.auth import get_user_model
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Страница пользователя')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pic', verbose_name='Аватар')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
