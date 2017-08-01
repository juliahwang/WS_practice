from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class UserProfileView(SessionAuthentication, BasicAuthentication):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        content = {
            'user': unicode()
        }
