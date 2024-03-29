# Generated by Django 4.1.1 on 2023-03-23 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0002_alter_rod_diameter_alter_rod_rod_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='measurement_scale',
        ),
        migrations.AddField(
            model_name='rodscalc',
            name='measurement_scale',
            field=models.SmallIntegerField(default=1, help_text='Во сколько раз вводимые значения больше действительных', verbose_name='Масштаб измерений'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Длина, мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='mass_of_rods',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Масса позиции, кг'),
        ),
    ]
