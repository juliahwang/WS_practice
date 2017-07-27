# from django.db import models
# from config import settings
#
# __all__ = (
#     'Music',
# )
#
#
# # 전체 음악파일/정보 모델
# class Music(models.Model):
#     WEATHER_CHOICES = (
#         ('sunny', '맑음'),
#         ('cloudy', '흐림'),
#         ('rainy', '비'),
#         ('snowy', '눈'),
#         ('foggy', '안개'),
#     )
#     name_author = models.ForeignKey(User, on_delete=models.CASCADE)
#     img_music = models.ImageField(upload_to='img_music', blank=True)
#     name_music = models.CharField(max_length=100)
#     name_singer = models.CharField(max_length=100)
#     file_music = models.FileField(upload_to='music')
#     name_album = models.CharField(max_length=100, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     tag_weather = models.ManyToManyField(
#         'Weather',
#         through='WeatherTag',
#         related_name='+',
#         choices=WEATHER_CHOICES,
#     )
#
#     def __str__(self):
#         return self.name_music
#
#
# # 날씨 분류
# class WeatherTag(models.Model):
#     tag_music = models.ForeignKey(Music, on_delete=models.PROTECT)
#     tag_weather = models.ForeignKey("Weather", on_delete=models.PROTECT)
#     sunny = models.IntegerField(verbose_name='맑음', default=1)
#     foggy = models.IntegerField(verbose_name='안개', default=1)
#     rainy = models.IntegerField(verbose_name='비', default=1)
#     cloudy = models.IntegerField(verbose_name='흐림', default=1)
#     snowy = models.IntegerField(verbose_name='눈', default=1)
#
#     class Meta:
#         unique_together = (
#             ('tag_music', 'tag_weather'),
#         )
#
#
# # 사용자의 위치를 받아와 날씨정보 ()시간마다 DB에 업데이트
# class Weather(models.Model):
#     latitude = models.FloatField(verbose_name='위도')
#     longitude = models.FloatField(verbose_name='경도')
#     location = models.CharField(max_length=100)
#     time_range = models.DateTimeField(auto_created=True)
#     name_area = models.CharField(max_length=100)
#     weather = models.CharField(max_length=100)
from django.contrib.auth import get_user_model
from django.db import models

__all__ = (
    'Music',
    'Weather'
)

User = get_user_model()


# 전체 음악파일/정보 모델
class Music(models.Model):
    name_author = models.ForeignKey(User, on_delete=models.CASCADE)
    img_music = models.ImageField(upload_to='img_music', blank=True)
    name_music = models.CharField(max_length=100)
    name_singer = models.CharField(max_length=100)
    file_music = models.FileField(upload_to='music')
    name_album = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    sunny = models.PositiveIntegerField(verbose_name='맑음', default=1)
    foggy = models.PositiveIntegerField(verbose_name='안개', default=1)
    rainy = models.PositiveIntegerField(verbose_name='비', default=1)
    cloudy = models.PositiveIntegerField(verbose_name='흐림', default=1)
    snowy = models.PositiveIntegerField(verbose_name='눈', default=1)

    def __str__(self):
        return self.name_music


# 사용자의 위치를 받아와 날씨정보 ()시간마다 DB에 업데이트
class Weather(models.Model):
    latitude = models.FloatField(verbose_name='위도')
    longitude = models.FloatField(verbose_name='경도')
    location = models.CharField(max_length=100)
    time_range = models.DateTimeField(auto_created=True)
    name_area = models.CharField(max_length=100)
    weather = models.CharField(max_length=100)


# 유저별 플레이리스트 모델
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_playlist = models.CharField(max_length=30, default='playlist')
    playlist_musics = models.ManyToManyField(
            'Music',
            through='PlaylistMusics',
            related_name='playlist_musics'
        )

    def __str__(self):
        return '{}의 {}'.format(
            self.user,
            self.name_playlist)


# 유저의 플레이리스트 내 음악 목록 모델
class PlaylistMusics(models.Model):
    name_playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    music = models.ForeignKey('Music', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '리스트 {}의 음악 {}'.format(
            self.name_playlist,
            self.music
        )
