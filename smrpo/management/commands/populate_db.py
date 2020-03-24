from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from smrpo.models.project import Project
from smrpo.models.project_user import ProjectUserRole

projects = {
    "Project 1.": "This is project 1.",
    "Test project": "Welcome to project test.",
    "Project 2": "Description is this.",
}

roles = [
    ["project_manager", "Project manager"],
    ["product_manager", "Product manager"],
    ["developer", "Developer"],
    ["methodology_master", "Methodology master"]
]

priorities = [
    "must have",
    "should have",
    "could have",
    "won't have this time"
]


class Command(BaseCommand):
    def handle(self, **options):
        admin = User.objects.get(username='admin')

        for project, description in projects.items():
            Project.objects.create(
                title=project,
                description=description,
                created_by=admin
            )

        for role in roles:
            ProjectUserRole.objects.create(
                title=role[1]
            )
