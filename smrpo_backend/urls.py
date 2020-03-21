from django.urls import path

from smrpo_backend.views.home import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]
