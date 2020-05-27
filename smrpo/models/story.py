from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    sprint = models.ForeignKey(Sprint, null=True, blank=True, on_delete=models.SET_NULL, related_name='stories')
    assigned_new_sprint = models.BooleanField(default=False)

    priority = models.ForeignKey(StoryPriority, on_delete=models.PROTECT)

    unique_by_project_count_id = models.IntegerField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_stories')
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
        # exclude finished, include tasks with assignee null
        return self.tasks.exclude(finished=True).filter(assignee__isnull=True).distinct()

    def get_assigned_tasks(self):
        # exclude finished, include tasks with assignee not null
        return self.tasks.exclude(finished=True).filter(assignee__isnull=False, active=False)

    # self.tasks.exclude(finished=True).filter(assignee__isnull=False, work_sessions__active__isnull=False).distinct()[0].work_sessions.filter(
        # active__isnull=True)

    def get_finished_tasks(self):
        return self.tasks.filter(finished=True).distinct()

    def get_active_tasks(self):
        # exclude finished, return tasks with active work sessions
        return self.tasks.exclude(finished=True).filter(active=True)

    @staticmethod
    def get_api_data(tasks):
        return [x.api_data for x in tasks]

    @property
    def api_data(self):
        return dict(
            id=self.id,
            unique_by_project_count_id=self.unique_by_project_count_id,
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


@receiver(post_save, sender=Story)
def story_post_save(sender, instance, created, **kwargs):

    if created:
        custom_id = instance.project.stories.count()
        instance.unique_by_project_count_id = custom_id
        instance.save()

    # TODO set this var somewhere, when new sprint assigned
    if instance.assigned_new_sprint:
        for task in instance.tasks.all():
            task.create_work_sessions()

        instance.assigned_new_sprint = False
        instance.save()
