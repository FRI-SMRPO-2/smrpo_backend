from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from smrpo.models.project import Project
from smrpo.models.sprint import Sprint


class StoryPriority(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Story priorities"

    def __str__(self):
        return self.name

    @property
    def api_data(self):
        return dict(
            id=self.id,
            name=self.name
        )


class StoryTest(models.Model):
    text = models.CharField(max_length=255)
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='tests')

    def __str__(self):
        return self.text


class Story(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    business_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    # set at the end of the sprint if all acceptance tests passed
    realized = models.BooleanField(default=False)
    time_complexity = models.FloatField(null=True, blank=True)
    rejection_comment = models.TextField(null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stories')
    sprint = models.ForeignKey(Sprint, null=True, blank=True, on_delete=models.CASCADE, related_name='stories')
    priority = models.ForeignKey(StoryPriority, on_delete=models.PROTECT)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='created_stories')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'project']
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.name

    def are_all_tasks_finished(self):
        return not self.tasks.filter(finished=False).exists()

    def get_unassigned_tasks(self):
        # exclude finished, exclude active, include tasks with assignee null
        return self.tasks.exclude(finished=True).exclude(active=True).filter(assignee__isnull=True)

    def get_assigned_tasks(self):
        # exclude finished, exclude active, include tasks with assignee not null
        return self.tasks.exclude(finished=True).exclude(active=True).filter(assignee__isnull=False)

    def get_finished_tasks(self):
        return self.tasks.filter(finished=True)

    def get_active_tasks(self):
        # exclude finished, return tasks with active=True
        return self.tasks.exclude(finished=True).filter(active=True)

    @staticmethod
    def get_api_data(tasks):
        return [x.api_data for x in tasks]

    @property
    def api_data(self):
        return dict(
            id=self.id,
            name=self.name,
            text=self.text,
            business_value=self.business_value,
            time_complexity=self.time_complexity,
            realized=self.realized,
            rejection_comment=self.rejection_comment if self.rejection_comment else None,
            all_tasks_finished=self.are_all_tasks_finished(),
            priority=self.priority.api_data,
            tests=list(self.tests.values('id', 'text')),
            project_id=self.project_id,
            created_by=self.created_by.username if self.created_by else None,
            created=self.created,
            updated=self.updated,
            tasks={
                'unassigned': Story.get_api_data(self.get_unassigned_tasks()),
                'assigned': Story.get_api_data(self.get_assigned_tasks()),
                'finished': Story.get_api_data(self.get_finished_tasks()),
                'active': Story.get_api_data(self.get_active_tasks())
            },
        )
