from django.contrib.auth import get_user_model, logout as django_logout, login as django_login
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from eyed3.compat import unicode
from rest_framework import generics, exceptions, status, parsers, renderers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import CustomAuthTokenSerializers, UserListSerializers
from django.utils.translation import ugettext_lazy as _


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


# class CustomBasicAuthentication(BasicAuthentication):
#     def authenticate(self, request):
#         """
#         BasicAuthentication의 authenticate 메서드 오버라이드.
#         facebook로그인을 위해 email validation을 수동으로 실행하고,
#         해당 email로 user를 가져오는 메서드.
#         """
#         user, _ = super(CustomBasicAuthentication, self).authenticate(request)
#         print(user)
#         email = user.email
#         # TODO facebook 로그인일 경우에는 해당 if문을 돌지 않도록 하기
#         if email and validate_email(email):
#             return email
#         elif _ is not None:
#             raise AuthenticationFailed('인증에 실패하였습니다. 다시 시도해주세요.')
#
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed('존재하지 않는 계정입니다.')
#         except not user.is_active:
#             raise exceptions.AuthenticationFailed('계정이 비활성화 상태입니다. 이메일을 확인하여 계정을 활성화하세요.')
#         return user


class CustomAuthTokenView(APIView):
    """
    Anonymous가 왔을 때 로그인을 시키고 token을 제공
    SessionAuthentication 실행
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomAuthTokenSerializers

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        return Response(content)

    # 테스트용 - 토큰 반환
    def post(self, request, format=None, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print('user: ', user)
        token, created = Token.objects.get_or_create(user=user)
        content = {
            'token': token.key,
            'email': user.email,
        }
        django_login(request, user)
        return Response(content)

        # token = self.get_token.post(request=request, *args, **kwargs)
        # print(token)
        # return token


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
    permission_classes = (AllowAny,)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (ObjectDoesNotExist, AttributeError):
            content = {
                "detail": _("No token given"),
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        django_logout(request)
        content = {
            "detail": _("Logged out"),
        }
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        return self.logout(request)
