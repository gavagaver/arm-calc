# Generated by Django 4.1.1 on 2022-12-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='title',
            field=models.CharField(max_length=70, verbose_name='Название'),
        ),
    ]