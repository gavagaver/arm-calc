# Generated by Django 4.1.1 on 2023-07-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0017_alter_rod_length_1_alter_rod_length_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rod',
            name='quantity_b',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Множитель M, шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_c',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Множитель N, шт'),
        ),
    ]
