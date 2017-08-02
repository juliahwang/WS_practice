import base64

import binascii
from django.contrib.auth import get_user_model, login as django_login
from django.core.validators import validate_email
from eyed3.compat import unicode
from rest_framework import generics, exceptions, HTTP_HEADER_ENCODING
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication, \
    BaseAuthentication, get_authorization_header
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserLoginSerializers

User = get_user_model()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializers
    permission_classes = (IsAuthenticated,)


class CustomBasicAuthentication(BasicAuthentication):

    def authenticate(self, request):
        user, _ = super(CustomBasicAuthentication, self).authenticate(request)
        email = request.META.get('email')
        if not email and validate_email(email):
            return None

        try:
            user = User.objects.get(email=email)
            django_login(request, user)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('존재하지 않는 계정입니다.')
        except not user.is_active:
            raise exceptions.AuthenticationFailed('계정이 비활성화 상태입니다. 이메일을 확인하세요.')
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
