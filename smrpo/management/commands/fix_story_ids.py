from django.core.management.base import BaseCommand

from smrpo.models.project import Project


class Command(BaseCommand):
    def handle(self, **options):

        for project in Project.objects.all():
            for i, story in enumerate(project.stories.order_by('created')):
                story.unique_by_project_count_id = i + 1
                story.save()
                print(f"updated project: {project.id} story id: {i + 1}")
