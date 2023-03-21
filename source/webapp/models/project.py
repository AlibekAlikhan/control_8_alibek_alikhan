from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Project(models.Model):
    start_at = models.DateField(verbose_name="Дата начала")
    users = models.ManyToManyField(to=User, related_name="project_users", blank=True)
    end_at = models.DateField(verbose_name="Дата конца", default=None)
    name = models.CharField(max_length=30, null=True, verbose_name="Имя")
    text_project = models.TextField(max_length=3000, null=True, verbose_name="Текст Проекта")
    iis_deleted = models.BooleanField(verbose_name="удалено", null=False, default=False)
    deleted_project_at = models.DateField(verbose_name="Дата удаления", null=True, default=None)

    def delete(self, using=None, keep_parents=False):
        self.iis_deleted = True
        self.deleted_project_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name



