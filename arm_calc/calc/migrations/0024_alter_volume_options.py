# Generated by Django 4.1.1 on 2024-03-14 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0023_alter_volume_is_hole'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='volume',
            options={'ordering': ('-create_date',), 'verbose_name': 'Объем', 'verbose_name_plural': 'Объемы'},
        ),
    ]