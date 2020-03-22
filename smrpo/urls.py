from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from smrpo.views.home import HomeView

# Create a router and register our viewsets with it.
from smrpo.views.project import ProjectViewSet

router = DefaultRouter()
router.register('project', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth', obtain_auth_token, name='api_token_auth'),
    path('', HomeView.as_view(), name="home"),
]
