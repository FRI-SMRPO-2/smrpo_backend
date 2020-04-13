from django.urls import path

from smrpo.views.current_sprint import ActiveSprintView
from smrpo.views.home import HomeView
from smrpo.views.project import ProjectView, ProjectsView, AuthProjectUserView
from smrpo.views.sprint import SprintsView, SprintView
from smrpo.views.sprint_stories import SprintStoriesView
from smrpo.views.story import StoriesView
from smrpo.views.token_authentication import TokenAuthenticationView
from smrpo.views.user import UsersView, AuthUserInfoView

urlpatterns = [
    path('auth', TokenAuthenticationView.as_view(), name='api_token_auth'),
    path('', HomeView.as_view(), name="home"),

    # User
    path('user/me/', AuthUserInfoView.as_view(), name="auth_user_info"),
    path('user/', UsersView.as_view(), name="users"),

    # Project
    path('project/', ProjectsView.as_view(), name="projects"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project"),
    path('project/<int:pk>/user/me/', AuthProjectUserView.as_view(), name="auth_project_user"),

    # Sprints
    path('project/<int:project_id>/sprint/', SprintsView.as_view(), name="sprints"),
    path('project/<int:project_id>/sprint/<int:sprint_id>/', SprintView.as_view(), name="sprint"),
    path('project/<int:project_id>/sprint/active', ActiveSprintView.as_view(), name="active_sprint"),

    # Project story
    path('project/<int:project_id>/story/', StoriesView.as_view(), name="stories"),

    # Sprint story
    path('sprint/<int:sprint_id>/story/', SprintStoriesView.as_view(), name="sprint_stories")
]
