from django.conf.urls import url
from music import views

urlpatterns = [
    url(r'^$', views.MusicListView.as_view(), name='musiclist'),
]