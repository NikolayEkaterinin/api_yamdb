# Generated by Django 3.2 on 2023-08-09 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20230809_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text='Расскажите о себе', verbose_name='Биография'),
        ),
    ]