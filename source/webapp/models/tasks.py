from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    status = models.ForeignKey('webapp.Status', related_name='tegs', on_delete=models.CASCADE, verbose_name="Статус")
    project = models.ForeignKey('webapp.Project', related_name='tegs', on_delete=models.CASCADE, verbose_name="Проект")
    teg = models.ManyToManyField(to="webapp.Teg", related_name="tegs", blank=True)
    text = models.TextField(max_length=3000, null=True, verbose_name="Текст")
    detail_text = models.TextField(max_length=3000, null=True, verbose_name="Детальный текст")
    iis_deleted = models.BooleanField(verbose_name="удалено", null=False, default=False)
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
        return f"{self.status} - {self.text}"
