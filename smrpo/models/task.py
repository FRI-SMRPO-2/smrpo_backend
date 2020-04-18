from django.conf import settings
from django.db import models

from smrpo.models.story import Story


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)

    active = models.BooleanField(default=False)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='assignee')
    finished = models.BooleanField(default=False)

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tasks')

    finished_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='finished_tasks')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tasks')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]

    def __str__(self):
        return "{} ({})".format(self.title, self.created_by)

    def finish(self, user):
        if self.assignee != user:
            return "Napaka pri zakljucevanju naloge. Uporabnik ni trenuten assignee!"

        self.finished = True
        self.finished_by = user
        self.save()

        return None

    @property
    def api_data(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            active=self.active,
            assignee=self.assignee.username if self.assignee else None,
            created_by=self.created_by.username if self.created_by else None,
            finished_by=self.finished_by.username if self.finished_by else None,
            finished=self.finished,
            created=self.created,
            updated=self.updated
        )
