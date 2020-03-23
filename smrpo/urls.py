from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from smrpo.views.home import HomeView
from smrpo.views.project import ProjectView


urlpatterns = [
    path('auth', obtain_auth_token, name='api_token_auth'),
    path('', HomeView.as_view(), name="home"),
    path('project/', ProjectView.as_view(), name="project"),
]
