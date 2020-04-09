from django.conf import settings
from django.db import models


class ProjectUser(models.Model):
    """
        Intermediate table for many to many field connecting projects with users.
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return "{} ({})".format(self.user.username, self.project_id)

    @property
    def api_data(self):
        return dict(
            id=self.id,
            # role=self.role.title,  # TODO could create a role property if needed
            name=self.user.get_full_name(),
            username=self.user.username,
            email=self.user.email,
        )
