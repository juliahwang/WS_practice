# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20170724_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]