# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='username',
        ),
        migrations.AddField(
            model_name='myuser',
            name='nickname',
            field=models.CharField(max_length=40, null=True, unique=True, verbose_name='nickname'),
        ),
    ]
