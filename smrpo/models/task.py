from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from smrpo.models.story import Story


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=40, default="open")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=False)

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tasks')

    finished_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='finished_tasks')
    canceled_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='canceled_tasks')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tasks')

    finished = models.DateTimeField(blank=True, null=True)
    closed = models.DateTimeField(blank=True, null=True)
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
        self.finished = timezone.now()
        self.finished_by = user
        self.save()


@receiver(post_save, sender=Task)
def task_post_save(sender, instance, *args, **kwargs):
    status = "open"

    if instance.finished:
        status = "finished"
    elif instance.users.exists():
        status = "pending"

    if status != instance.status:
        instance.update(status=status)
