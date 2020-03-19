from django.conf import settings
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=255, null=True, blank=True)

    deadline = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    canceled = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

