# Generated by Django 4.1.1 on 2022-11-26 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('calc', '0002_alter_rod_element'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='engineer',
        ),
        migrations.AddField(
            model_name='element',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='account.folder', verbose_name='Папка'),
        ),
    ]
