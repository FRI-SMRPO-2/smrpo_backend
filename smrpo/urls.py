from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from smrpo.views.home import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('auth', obtain_auth_token, name='api_token_auth'),
]
