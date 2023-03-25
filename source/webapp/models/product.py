from django.contrib.auth.models import User
from django.db import models
from django.db.models import TextChoices
from django.utils import timezone


class CategoryChoice(TextChoices):
    OTHER = 'other', 'разное'
    TECHNIQUE = 'technique', 'техника'
    CLOTH = 'cloth', 'одежда'
    TOYS = 'toys', 'игрушки'


class Product(models.Model):
    category = models.CharField(verbose_name="Категория", choices=CategoryChoice.choices, max_length=20,
                                default=CategoryChoice.OTHER)
    name = models.CharField(max_length=100, null=False, verbose_name="Имя")
    text = models.TextField(max_length=2000, null=True, verbose_name="Текст")
    iis_deleted = models.BooleanField(verbose_name="удалено", null=False, default=False)
    image_url = models.TextField(max_length=3000, null=True, verbose_name="Фото")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    update_at = models.DateTimeField(verbose_name="Дата обновления", null=True, default=None)
    deleted_at = models.DateField(verbose_name="Дата удаления", null=True, default=None)

    def update(self, using=None, keep_parents=False):
        self.update_at = timezone.now()
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.iis_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.category} - {self.text}"
