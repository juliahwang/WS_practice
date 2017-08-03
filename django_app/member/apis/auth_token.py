from django.contrib.auth import get_user_model, logout as django_logout, login as django_login
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from eyed3.compat import unicode
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import CustomAuthTokenSerializers, UserListSerializers

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
