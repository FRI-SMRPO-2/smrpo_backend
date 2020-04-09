from django.conf import settings
from django.db import models

from smrpo.models.project_user import ProjectUser


class Project(models.Model):
    name = models.CharField(max_length=60, unique=True)
    documentation = models.TextField(null=True, blank=True)

    # project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    project_owner = models.ForeignKey(ProjectUser, on_delete=models.CASCADE, related_name="project_owner")
    scrum_master = models.ForeignKey(ProjectUser, on_delete=models.CASCADE, related_name="scrum_master")
    developers = models.ManyToManyField(ProjectUser, related_name="developers")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='created_projects')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def api_data(self):
        return dict(
            id=self.id,
            name=self.name,
            documentation=self.documentation,
            scrum_master=self.scrum_master.api_data,
            project_owner=self.project_owner.api_data,
            developers=[user.api_data for user in self.developers.all()],
            created_by=self.created_by.username,
            created=self.created,
            updated=self.updated,
        )
