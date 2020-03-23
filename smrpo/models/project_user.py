from django.conf import settings
from django.db import models


class ProjectUserRole(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description


class ProjectUser(models.Model):
    """
        Intermediate table for many to many field connecting projects with users.
    """
    role = models.ForeignKey(ProjectUserRole, on_delete=models.DO_NOTHING)

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def api_data(self):
        return dict(
            id=self.id,
            role=self.role.title,
            name=self.user.get_full_name(),
            username=self.user.username,
            email=self.user.email,
        )
