from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from smrpo.views.home import HomeView
from smrpo.views.project import ProjectView, ProjectsView
from smrpo.views.project_role import ProjectRolesView
from smrpo.views.sprint import SprintsView, SprintView
from smrpo.views.user import UsersView, AuthUserInfoView

urlpatterns = [
    path('auth', obtain_auth_token, name='api_token_auth'),
    path('', HomeView.as_view(), name="home"),

    # User
    path('user/me/', AuthUserInfoView.as_view(), name="auth_user_info"),
    path('user/', UsersView.as_view(), name="users"),

    # Project
    path('project/', ProjectsView.as_view(), name="projects"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project"),

    # Sprints
    path('project/<int:project_id>/sprint/', SprintsView.as_view(), name="sprints"),
    path('project/<int:project_id>/sprint/<int:sprint_id>/', SprintView.as_view(), name="sprint"),

    # Project roles
    path('project_role/', ProjectRolesView.as_view(), name="project_roles"),
]
