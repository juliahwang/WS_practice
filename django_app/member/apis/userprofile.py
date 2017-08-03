import base64

import binascii

import requests
from django.contrib.auth import get_user_model, login as django_login
from django.core.validators import validate_email
from eyed3.compat import unicode
from rest_framework import generics, exceptions, HTTP_HEADER_ENCODING, authentication, status, parsers, renderers
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication, \
    BaseAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
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
        print(user)
        email = user.email
        # TODO facebook 로그인일 경우에는 해당 if문을 돌지 않도록 하기
        if email and validate_email(email):
            return email
        elif auth is not None:
            raise AuthenticationFailed('인증에 실패하였습니다. 다시 시도해주세요.')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('존재하지 않는 계정입니다.')
        except not user.is_active:
            raise exceptions.AuthenticationFailed('계정이 비활성화 상태입니다. 이메일을 확인하여 계정을 활성화하세요.')
        return user, auth


class UserLoginView(APIView):
    """
    Anonymous가 왔을 때 로그인을 시키고 token을 제공
    SessionAuthentication 실행
    """
    authentication_classes = (SessionAuthentication, CustomBasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLoginSerializers
    # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    # renderer_classes = (renderers.JSONRenderer,)
    # get_token = ObtainAuthToken()

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        return Response(content)

    # 테스트용 - 토큰 반환
    def post(self, request, format=None, *args, **kwargs):
        parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
        renderer_classes = (renderers.JSONRenderer,)
        self.serializer_class = AuthTokenSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

        # token = self.get_token.post(request=request, *args, **kwargs)
        # print(token)
        # return token

    #
    #     def get_token_included_url(token):
    #         url_user_info = 'https://localhost:8000/api/member/login Authentication: Token {token}'.format(
    #             token=token,
    #         )
    #         url_user_params = {
    #             'token': token,
    #             'fields': ','.join([
    #                 'email',
    #                 'password',
    #             ])
    #         }
    #         response = requests.get(url_user_info, params=url_user_params)
    #         result = response.json()
    #         return result
    #     try:
    #         email = request.POST['email']
    #         print(email)
    #         user = User.objects.get(email=email)
    #         print(user)
    #         user.authenticate(request)
    #         django_login(request, user)
    #         get_token_included_url(token=request.user.auth_token)
    #         content = {
    #             'email': user.email,
    #             'password': user.password,
    #         }
    #     except User.DoesNotExist:
    #         raise AuthenticationFailed('존재하지 않는 계정입니다.')
    #     return Response(content)


class UserLogoutView(APIView):
    queryset = User.objects.all()

    def get(self, request):
        request.user.auth_token.delete()
        return Response(request, status=status.HTTP_200_OK)
