# Generated by Django 4.1.6 on 2023-03-21 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateField(verbose_name='Дата начала')),
                ('end_at', models.DateField(default=None, verbose_name='Дата конца')),
                ('name', models.CharField(max_length=30, null=True, verbose_name='Имя')),
                ('text_project', models.TextField(max_length=3000, null=True, verbose_name='Текст Проекта')),
                ('iis_deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('deleted_project_at', models.DateField(default=None, null=True, verbose_name='Дата удаления')),
                ('users', models.ManyToManyField(blank=True, related_name='project_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Teg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Тег')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=3000, null=True, verbose_name='Текст')),
                ('detail_text', models.TextField(max_length=3000, null=True, verbose_name='Детальный текст')),
                ('iis_deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('update_at', models.DateTimeField(default=None, null=True, verbose_name='Дата обновления')),
                ('deleted_at', models.DateField(default=None, null=True, verbose_name='Дата удаления')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tegs', to='webapp.project', verbose_name='Проект')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tegs', to='webapp.status', verbose_name='Статус')),
                ('teg', models.ManyToManyField(blank=True, related_name='tegs', to='webapp.teg')),
            ],
        ),
    ]
