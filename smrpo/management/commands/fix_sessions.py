import datetime

from django.core.management.base import BaseCommand

from smrpo.models.task import Task


class Command(BaseCommand):
    def handle(self, **options):

        for task in Task.objects.filter(story__sprint__isnull=False):

            # Create WorkSessions for every sprint day for every user
            print(f"\n {task}")
            task.create_work_sessions()
