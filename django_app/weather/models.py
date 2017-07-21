from django.db import models


# 날씨 분류
class WeatherTag(models.Model):
    weather1 = models.IntegerField()
    weather2 = models.IntegerField()
    weather3 = models.IntegerField()
    weather4 = models.IntegerField()
    weather5 = models.IntegerField()


# 사용자의 위치를 받아와 날씨정보 4시간마다 DB에 업데이트
class Weather(models.Model):
    latitude = models.FloatField(verbose_name='위도')
    longitude = models.FloatField(verbose_name='경도')
    location = models.CharField(max_length=100)
    time_range = models.DateTimeField(auto_created=True)
    name_area = models.CharField(max_length=100)
    weather = models.CharField(max_length=100)

