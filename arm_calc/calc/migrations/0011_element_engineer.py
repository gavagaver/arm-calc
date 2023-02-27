# Generated by Django 4.1.1 on 2023-02-27 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calc', '0010_alter_rod_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='engineer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='elements', to=settings.AUTH_USER_MODEL, verbose_name='Инженер'),
        ),
    ]