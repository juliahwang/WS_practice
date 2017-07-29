from rest_framework.response import Response
from rest_framework.views import APIView
from music.models import Music
from music.serializers import MusicSerializer


class MusicListCreateView(APIView):
    def get(self, request, *args, *kwargs):
        musics = Music.objects.all()
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data)
