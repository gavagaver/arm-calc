# Generated by Django 4.1.1 on 2023-07-13 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0018_alter_rod_quantity_b_alter_rod_quantity_c'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rod',
            name='quantity_a',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Множитель F, шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_b',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Множитель G, шт'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='quantity_c',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Множитель H, шт'),
        ),
    ]
