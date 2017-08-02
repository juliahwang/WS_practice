from django.contrib.auth import get_user_model, login as django_login
from eyed3.compat import unicode
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication, \
    BaseAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserLoginSerializers

User = get_user_model()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializers


class CustomBasicAuthentication(BasicAuthentication):

    def authenticate(self, request):
        user, _ = super(CustomBasicAuthentication, self).authenticate(request)

        django_login(request, user)
        return user, _


class UserLoginView(APIView):
    authentication_classes = (SessionAuthentication, CustomBasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_classes = UserLoginSerializers

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        return Response(content)
