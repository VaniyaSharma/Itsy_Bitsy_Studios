# Generated by Django 5.0 on 2024-03-25 02:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.IntegerField()),
                ('event_title', models.CharField(max_length=200)),
                ('time', models.TimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_app.trip')),
            ],
        ),
    ]
