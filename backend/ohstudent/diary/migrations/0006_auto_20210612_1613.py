# Generated by Django 3.2 on 2021-06-12 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_auto_20210612_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time_from',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_to',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]