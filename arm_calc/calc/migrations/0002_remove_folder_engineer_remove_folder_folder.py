# Generated by Django 4.1.1 on 2023-03-17 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='engineer',
        ),
        migrations.RemoveField(
            model_name='folder',
            name='folder',
        ),
    ]
