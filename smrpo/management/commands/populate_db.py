from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from smrpo.models.project import Project
from smrpo.models.project_user import ProjectUserRole
from smrpo.models.story import StoryPriority

projects = {
    "Project 1.": "This is project 1.",
    "Test project": "Welcome to project test.",
    "Project 2": "Description is this.",
}

roles = [
    ["product_owner", "Product Owner"],
    ["scrum_master", "Scrum Master"],
    ["developer", "Developer"]
]

priorities = [
    "Must have",
    "Should have",
    "Could have",
    "Won't have this time"
]


class Command(BaseCommand):
    def handle(self, **options):
        admin = User.objects.get(username='admin')

        # for project, description in projects.items():
        #     Project.objects.create(
        #         name=project,
        #         created_by=admin
        #     )
        #
        # for role in roles:
        #     ProjectUserRole.objects.create(
        #         title=role[1]
        #     )

        for priority in priorities:
            StoryPriority.objects.create(
                text=priority
            )
