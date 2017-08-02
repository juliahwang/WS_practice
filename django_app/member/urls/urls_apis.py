from django.conf.urls import url
from rest_framework.authtoken import views as rest_views
from member import views, apis

urlpatterns = [
    url(r'^users/', apis.UserListView.as_view()),
    url(r'^api-token-auth/', rest_views.obtain_auth_token),
    url(r'^signup/$', views.signup, name='signup'),
    # url(r'^login/$', views.login, name='login'),
    url(r'^login/$', apis.UserLoginView.as_view(), name='login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate')
]
