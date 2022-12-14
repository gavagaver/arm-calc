# Generated by Django 4.1.1 on 2022-12-02 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0006_alter_rod_arm_class_alter_rod_diameter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rod',
            name='arm_class',
            field=models.CharField(blank=True, default='Класс арматуры', max_length=150, null=True, verbose_name='Класс арматуры'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='diameter',
            field=models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Диаметр'),
        ),
        migrations.AlterField(
            model_name='rod',
            name='length',
            field=models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Длина'),
        ),
    ]
