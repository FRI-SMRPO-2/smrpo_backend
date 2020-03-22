from django.conf import settings
from django.db import models

from smrpo.models.project_user import ProjectUser


class Project(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=255, null=True, blank=True)

    deadline = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    canceled = models.DateTimeField(blank=True, null=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through=ProjectUser, related_name='projects')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='created_projects')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

