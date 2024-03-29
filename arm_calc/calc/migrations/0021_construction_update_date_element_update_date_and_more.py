# Generated by Django 4.1.1 on 2023-09-02 18:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0020_remove_rodscalc_measurement_scale_rodscalc_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='construction',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='element',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='folder',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rod',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rodclass',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roddiameter',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rodscalc',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='version',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата последнего изменения'),
            preserve_default=False,
        ),
    ]
