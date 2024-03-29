# Generated by Django 4.1.1 on 2023-06-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0005_alter_rodclass_total_mass_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rod',
            name='diameter',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Диаметр, мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Длина, мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length_1',
            field=models.PositiveSmallIntegerField(verbose_name='Длина 1 уч., мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length_2',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Длина 2 уч., мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length_3',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Длина 3 уч., мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length_4',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Длина 4 уч., мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Кол-во, шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_1',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Кол-во 1 уч., шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_2',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Кол-во 2 уч., шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_3',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Кол-во 3 уч., шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_4',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Кол-во 4 уч., шт'),
        ),
        migrations.AlterField(
            model_name='rodscalc',
            name='measurement_scale',
            field=models.PositiveSmallIntegerField(default=1, help_text='Во сколько раз вводимые значения больше действительных', verbose_name='Масштаб измерений'),
        ),
    ]
