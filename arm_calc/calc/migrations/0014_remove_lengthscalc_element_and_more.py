# Generated by Django 4.1.1 on 2023-06-16 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0013_alter_rod_length_1_alter_rod_length_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lengthscalc',
            name='element',
        ),
        migrations.RemoveField(
            model_name='square',
            name='squares_calc',
        ),
        migrations.RemoveField(
            model_name='squarescalc',
            name='element',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='units_calc',
        ),
        migrations.RemoveField(
            model_name='unitscalc',
            name='element',
        ),
        migrations.RemoveField(
            model_name='volume',
            name='volumes_calc',
        ),
        migrations.RemoveField(
            model_name='volumescalc',
            name='element',
        ),
        migrations.DeleteModel(
            name='Length',
        ),
        migrations.DeleteModel(
            name='LengthsCalc',
        ),
        migrations.DeleteModel(
            name='Square',
        ),
        migrations.DeleteModel(
            name='SquaresCalc',
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
        migrations.DeleteModel(
            name='UnitsCalc',
        ),
        migrations.DeleteModel(
            name='Volume',
        ),
        migrations.DeleteModel(
            name='VolumesCalc',
        ),
    ]