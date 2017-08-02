import base64

import binascii
from django.contrib.auth import get_user_model, login as django_login
from django.core.validators import validate_email
from eyed3.compat import unicode
from rest_framework import generics, exceptions, HTTP_HEADER_ENCODING, authentication
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication, \
    BaseAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserLoginSerializers, UserListSerializers

User = get_user_model()


class UserListView(generics.ListCreateAPIView):
    """
    유저 리스트
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserListSerializers

    def pre_save(self, obj):
        if self.request.user.is_admin:
            obj.owner = self.request.user


class CustomBasicAuthentication(BasicAuthentication):

    def authenticate(self, request):
        """
        BasicAuthentication의 authenticate 메서드 오버라이드.
        facebook로그인을 위해 email validation을 수동으로 실행하고,
        해당 email로 user를 가져오는 메서드.
        """
        user, auth = super(CustomBasicAuthentication, self).authenticate(request)
        email = request.META.get('email')
        # TODO facebook 로그인일 경우에는 해당 if문을 돌지 않도록 하기
        if not email and validate_email(email):
            return None
        elif auth is not None:
            raise AuthenticationFailed('인증에 실패하였습니다. 다시 시도해주세요.')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('존재하지 않는 계정입니다.')
        except not user.is_active:
            raise exceptions.AuthenticationFailed('계정이 비활성화 상태입니다. 이메일을 확인하여 계정을 활성화하세요.')
        return user, auth

    def authenticate_header(self, request):
        pass


class UserLoginView(APIView):
    """
    SessionAuthentication 실행
    """
    authentication_classes = (SessionAuthentication, CustomBasicAuthentication)
    permission_classes = (AllowAny,)
    serializer_classes = UserLoginSerializers
    token_model = Token

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        return Response(content)

    def post(self, request, format=None):
        user = User.objects.get(pk=self.request.user.pk)
        content = {
            'email': user.email,
            'password': user.password,
        }
        return Response(content)
