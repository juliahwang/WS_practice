from django.conf.urls import url
from music import apis

urlpatterns = [
    url(r'^$', apis.MusicListView.as_view(), name='musiclist'),
]