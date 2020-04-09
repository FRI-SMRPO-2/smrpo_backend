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

    def __str__(self):
        return "{} ({})".format(self.user.username, self.project_id)

    @property
    def roles(self):
        roles = []
        if self == self.project.product_owner:
            roles.append("Product Owner")
        if self == self.project.scrum_master:
            roles.append("Scrum Master")
        if self.project.developers.filter(id=self.id).exists():
            roles.append("Developer")
        return roles

    @property
    def api_data(self):
        return dict(
            id=self.id,
            role=self.roles,
            name=self.user.get_full_name(),
            username=self.user.username,
            email=self.user.email,
        )
