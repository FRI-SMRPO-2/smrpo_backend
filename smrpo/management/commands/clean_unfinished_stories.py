from django.core.management.base import BaseCommand
from django.utils import timezone

from smrpo.models.story import Story


class Command(BaseCommand):
    def handle(self, **options):
        now = timezone.now()
        unfinished_stories = Story.objects.filter(sprint__isnull=False, sprint__end_date__lt=now, realized__isnull=True)
        unfinished_stories.update(sprint=None)
