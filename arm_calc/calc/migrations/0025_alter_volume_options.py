# Generated by Django 4.1.1 on 2024-03-14 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0024_alter_volume_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='volume',
            options={'ordering': ('create_date',), 'verbose_name': 'Объем', 'verbose_name_plural': 'Объемы'},
        ),
    ]