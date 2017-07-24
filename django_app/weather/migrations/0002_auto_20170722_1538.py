# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weathertag',
            name='weather1',
        ),
        migrations.RemoveField(
            model_name='weathertag',
            name='weather2',
        ),
        migrations.RemoveField(
            model_name='weathertag',
            name='weather3',
        ),
        migrations.RemoveField(
            model_name='weathertag',
            name='weather4',
        ),
        migrations.RemoveField(
            model_name='weathertag',
            name='weather5',
        ),
        migrations.AddField(
            model_name='weathertag',
            name='cloudy',
            field=models.IntegerField(default=0, verbose_name='흐림'),
        ),
        migrations.AddField(
            model_name='weathertag',
            name='foggy',
            field=models.IntegerField(default=0, verbose_name='안개'),
        ),
        migrations.AddField(
            model_name='weathertag',
            name='rainy',
            field=models.IntegerField(default=0, verbose_name='비'),
        ),
        migrations.AddField(
            model_name='weathertag',
            name='snowy',
            field=models.IntegerField(default=0, verbose_name='눈'),
        ),
        migrations.AddField(
            model_name='weathertag',
            name='sunny',
            field=models.IntegerField(default=0, verbose_name='맑음'),
        ),
    ]
