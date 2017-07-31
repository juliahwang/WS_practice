# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 03:41
from __future__ import unicode_literals

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
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_music', models.ImageField(blank=True, upload_to='img_music')),
                ('name_music', models.CharField(max_length=100)),
                ('name_singer', models.CharField(max_length=100)),
                ('file_music', models.FileField(upload_to='music')),
                ('name_album', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('sunny', models.PositiveIntegerField(default=1, verbose_name='맑음')),
                ('foggy', models.PositiveIntegerField(default=1, verbose_name='안개')),
                ('rainy', models.PositiveIntegerField(default=1, verbose_name='비')),
                ('cloudy', models.PositiveIntegerField(default=1, verbose_name='흐림')),
                ('snowy', models.PositiveIntegerField(default=1, verbose_name='눈')),
                ('name_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_playlist', models.CharField(default='playlist', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistMusics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Music')),
                ('name_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Playlist')),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_range', models.DateTimeField(auto_created=True)),
                ('latitude', models.FloatField(verbose_name='위도')),
                ('longitude', models.FloatField(verbose_name='경도')),
                ('location', models.CharField(max_length=100)),
                ('name_area', models.CharField(max_length=100)),
                ('weather', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist_musics',
            field=models.ManyToManyField(related_name='playlist_musics', through='music.PlaylistMusics', to='music.Music'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
