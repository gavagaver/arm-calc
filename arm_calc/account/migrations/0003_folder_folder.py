# Generated by Django 4.1.1 on 2023-02-27 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_folder_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='folders', to='account.folder', verbose_name='Инженер'),
        ),
    ]