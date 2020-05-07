from django.core.management.base import BaseCommand
from django.utils import timezone

from smrpo.models.story import Story
from smrpo.models.task import Task


class Command(BaseCommand):
    def handle(self, **options):
        now = timezone.now()
        unfinished_stories = Story.objects.filter(sprint__isnull=False, sprint__end_date__lt=now, realized=False)
        updated = unfinished_stories.update(
            sprint=None,
            rejection_comment="Zgodba ni bila realizirana do konca aktivnega sprinta."
        )

        print(f"Cleaned {updated} unfinished stories.")

        # Only temporary
        tasks = Task.objects.filter(story__sprint__end_date__lt=now, assignee_awaiting__isnull=False)
        updated = tasks.update(assignee_awaiting=None)
        print(f"Cleaned {updated} unfinished tasks.")

        for story in unfinished_stories:
            story.tasks.filter(assignee_awaiting__isnull=False).update(assignee_awaiting=None)

