# Generated by Django 3.2 on 2021-05-28 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, choices=[('private', 'private'), ('public', 'public')], default='private', max_length=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
