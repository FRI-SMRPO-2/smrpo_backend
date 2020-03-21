from django.conf import settings
from django.db import models


class ProjectMemberRole(models.Model):
    role = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)


class ProjectMember(models.Model):
    """
        Intermediate table for many to many field connecting projects with members.
    """
    title = models.CharField(max_length=60)
    role = models.ForeignKey(ProjectMemberRole, on_delete=models.DO_NOTHING)

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
