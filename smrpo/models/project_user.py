from django.conf import settings
from django.db import models


class ProjectUserRole(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class ProjectUser(models.Model):
    """
        Intermediate table for many to many field connecting projects with users.
    """
    role = models.ForeignKey(ProjectUserRole, on_delete=models.DO_NOTHING)

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
