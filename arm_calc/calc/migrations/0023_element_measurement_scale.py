# Generated by Django 4.1.1 on 2023-03-04 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0022_alter_rod_length_2_alter_rod_quantity_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='measurement_scale',
            field=models.SmallIntegerField(default=1, help_text='Во сколько раз вводимые значения больше действительных', verbose_name='Масштаб измерений'),
        ),
    ]
