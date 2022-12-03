# Generated by Django 4.1.1 on 2022-12-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0008_rod_quantity_alter_rod_diameter_alter_rod_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='title',
            field=models.CharField(max_length=70, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='arm_class',
            field=models.CharField(blank=True, default='Класс арматуры', max_length=50, null=True, verbose_name='Класс арматуры'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='title',
            field=models.CharField(max_length=70, verbose_name='Название'),
        ),
    ]
