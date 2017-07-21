from django.db import models
from config import settings


# 전체 음악파일/정보 모델
class Music(models.Model):
    WEATHER_CHOICES = (
        ('sunny', '맑음'),
        ('cloudy', '흐림'),
        ('rainy', '비'),
        ('snowy', '눈'),
        ('foggy', '안개'),
    )
    name_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name_music = models.CharField(max_length=100)
    name_singer = models.CharField(max_length=100)
    file_music = models.FileField()
    name_album = models.CharField(max_length=100)
    date_released = models.DateField(auto_now_add=True)
    tag_weather = models.CharField(max_length=1000)
