from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from smrpo.views.home import HomeView
from smrpo.views.project import ProjectView, ProjectsView
from smrpo.views.project_role import ProjectRolesView
from smrpo.views.sprint import SprintsView
from smrpo.views.user import UsersView

urlpatterns = [
    path('auth', obtain_auth_token, name='api_token_auth'),
    path('', HomeView.as_view(), name="home"),

    # User
    path('user/', UsersView.as_view(), name="users"),

    # Project
    path('project/', ProjectsView.as_view(), name="projects"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project"),

    # Project roles
    path('project_role/', ProjectRolesView.as_view(), name="project_roles"),

    # Sprints
    path('sprint/', SprintsView.as_view(), name="sprints")
]
