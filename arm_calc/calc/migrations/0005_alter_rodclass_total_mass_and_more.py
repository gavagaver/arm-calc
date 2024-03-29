# Generated by Django 4.1.1 on 2023-06-12 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0004_alter_rod_mass_of_rods_alter_rod_mass_of_single_rod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rodclass',
            name='total_mass',
            field=models.FloatField(blank=True, null=True, verbose_name='Всего, кг'),
        ),
        migrations.AlterField(
            model_name='roddiameter',
            name='total_mass',
            field=models.FloatField(blank=True, null=True, verbose_name='Всего, кг'),
        ),
        migrations.AlterField(
            model_name='rodscalc',
            name='total_mass',
            field=models.FloatField(blank=True, null=True, verbose_name='Всего, кг'),
        ),
    ]
