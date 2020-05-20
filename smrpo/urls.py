from django.urls import path

from smrpo.views.current_sprint import ActiveSprintView
from smrpo.views.documentation import DocumentationView
from smrpo.views.post import PostView
from smrpo.views.project import ProjectView, ProjectsView, AuthProjectUserView
from smrpo.views.realize_stories import RealizeStoriesView
from smrpo.views.reject_stories import RejectStoriesView
from smrpo.views.sprint import SprintsView, SprintView
from smrpo.views.sprint_stories import SprintStoriesView
from smrpo.views.story import StoriesView, StoryView
from smrpo.views.task import StoryTasksView, FinishTaskView, AcceptTaskView, DeclineTaskView, StartWorkTaskView, StopWorkTaskView
from smrpo.views.task_work_sessions import TaskWorkSessionsView
from smrpo.views.token_authentication import TokenAuthenticationView
from smrpo.views.user import UsersView, AuthUserInfoView, AuthUserTasksView

urlpatterns = [
    path('auth', TokenAuthenticationView.as_view(), name='api_token_auth'),

    # User
    path('user/me/', AuthUserInfoView.as_view(), name="auth_user_info"),
    path('user/me/tasks', AuthUserTasksView.as_view(), name="auth_user_tasks"),
    path('user/', UsersView.as_view(), name="users"),

    # Project
    path('project/', ProjectsView.as_view(), name="projects"),
    path('project/<int:pk>', ProjectView.as_view(), name="project"),
    path('project/<int:pk>/user/me/', AuthProjectUserView.as_view(), name="auth_project_user"),

    # Sprints
    path('project/<int:project_id>/sprint/', SprintsView.as_view(), name="sprints"),
    path('project/<int:project_id>/sprint/<int:sprint_id>', SprintView.as_view(), name="sprint"),
    path('project/<int:project_id>/sprint/active', ActiveSprintView.as_view(), name="active_sprint"),

    # User story
    path('project/<int:project_id>/story/<int:story_id>', StoryView.as_view(), name="story"),
    path('project/<int:project_id>/story/realize', RealizeStoriesView.as_view(), name="realize_stories"),
    path('project/<int:project_id>/story/reject', RejectStoriesView.as_view(), name="reject_stories"),

    # Tasks
    path('story/<int:story_id>/task/', StoryTasksView.as_view(), name="story_tasks"),
    path('task/<int:task_id>/finish', FinishTaskView.as_view(), name="finish_task"),
    path('task/<int:task_id>/accept', AcceptTaskView.as_view(), name="accept_task"),
    path('task/<int:task_id>/decline', DeclineTaskView.as_view(), name="decline_task"),
    path('task/<int:task_id>/start_work', StartWorkTaskView.as_view(), name="start_work_task"),
    path('task/<int:task_id>/stop_work', StopWorkTaskView.as_view(), name="stop_work_task"),
    path('task/<int:task_id>/work_sessions', TaskWorkSessionsView.as_view(), name="task_work_sessions"),

    # Project story
    path('project/<int:project_id>/story/', StoriesView.as_view(), name="stories"),

    # Project posts
    path('project/<int:project_id>/post/', PostView.as_view(), name="posts"),

    # Project documentation
    path('project/<int:project_id>/documentation/', DocumentationView.as_view(), name="documentation"),

    # Sprint story
    path('sprint/<int:sprint_id>/story/', SprintStoriesView.as_view(), name="sprint_stories"),
]
