# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20170722_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='tag_weather',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='weather.WeatherTag'),
        ),
    ]