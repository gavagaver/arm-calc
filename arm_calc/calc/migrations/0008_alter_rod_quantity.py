# Generated by Django 4.1.1 on 2023-06-12 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0007_alter_rod_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rod',
            name='quantity',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Кол-во, шт'),
        ),
    ]