# Generated by Django 4.1.1 on 2023-06-12 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0011_rod_length_3_rod_quantity_3_alter_rod_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rod',
            name='length_1',
            field=models.SmallIntegerField(verbose_name='Длина 1 уч., мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length_2',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Длина 2 уч., мм'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_1',
            field=models.SmallIntegerField(default=1, verbose_name='Кол-во 1 уч., шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_2',
            field=models.SmallIntegerField(blank=True, default=1, null=True, verbose_name='Кол-во 2 уч., шт'),
        ),
    ]
