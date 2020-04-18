from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from smrpo.forms import UserCreateForm
from smrpo.models.project import Project
from smrpo.models.story import StoryPriority

projects = {
    "Project 1.": "This is project 1.",
    "Test project": "Welcome to project test.",
    "Project 2": "Description is this.",
}

priorities = [
    "Must have",
    "Should have",
    "Could have",
    "Won't have this time"
]


class Command(BaseCommand):
    def handle(self, **options):
        for priority in priorities:
            StoryPriority.objects.create(
                name=priority
            )

        user = dict(
            first_name="Admin",
            last_name="Adminovic",
            username="admin",
            email="admin@gmail.com",
            password1="test12345",
            password2="test12345",
            is_superuser=True,
            is_staff=True
        )
        form = UserCreateForm(user)
        if form.is_valid():
            user = form.save()

        user = dict(
            first_name="Janez",
            last_name="Novak",
            username="janez.novak",
            email="janez.novak@gmail.com",
            password1="test12345",
            password2="test12345"
        )
        form = UserCreateForm(user)
        if form.is_valid():
            user = form.save()

        p = Project.objects.create(
            name="Project #1",
            documentation="Dokumentacija prvega projekta.",
            scrum_master_id=1,
            product_owner_id=1,
            created_by_id=1,
        )

        p.developers.set([1, 2])
        p.save()

        Token.objects.create(
            user_id=1,
            key="e76859b708545d3c06dd794d604b287a934ce7a8"
        )
        Token.objects.create(
            user_id=2,
            key="5660ec0e8e53066c8856d9494f5dc663f06b793b"
        )
