from django.conf import settings
from django.db import models

from smrpo.models.project import Project


class Post(models.Model):
    text = models.TextField(null=False, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True,
                                   related_name='created_posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='posts')

    @property
    def api_data(self):
        return dict(
            id=self.id,
            text=self.text,
            project_id=self.project_id,
            created_by=self.created_by.username,
            created=self.created,
            updated=self.updated
        )
