# Generated by Django 2.2 on 2020-09-14 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='git',
            field=models.TextField(default='None', max_length=100, verbose_name='Ссылка'),
        ),
        migrations.AddField(
            model_name='profile',
            name='self',
            field=models.TextField(default='None', max_length=300, verbose_name='О себе'),
        ),
    ]
