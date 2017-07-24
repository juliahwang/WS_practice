from django.db import models


# 날씨 분류
class WeatherTag(models.Model):
    WEATHER_CHOICES = (
        ('sunny', '맑음'),
        ('cloudy', '흐림'),
        ('rainy', '비'),
        ('snowy', '눈'),
        ('foggy', '안개'),
    )
    tag_weather = models.CharField(max_length=2, default='sunny', choices=WEATHER_CHOICES)
    sunny = models.IntegerField(verbose_name='맑음', default=0)
    foggy = models.IntegerField(verbose_name='안개', default=0)
    rainy = models.IntegerField(verbose_name='비', default=0)
    cloudy = models.IntegerField(verbose_name='흐림', default=0)
    snowy = models.IntegerField(verbose_name='눈', default=0)


# 사용자의 위치를 받아와 날씨정보 ()시간마다 DB에 업데이트
class Weather(models.Model):
    latitude = models.FloatField(verbose_name='위도')
    longitude = models.FloatField(verbose_name='경도')
    location = models.CharField(max_length=100)
    time_range = models.DateTimeField(auto_created=True)
    name_area = models.CharField(max_length=100)
    weather = models.CharField(max_length=100)

