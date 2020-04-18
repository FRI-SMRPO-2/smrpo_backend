from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=60, unique=True)
    documentation = models.TextField(null=True, blank=True)

    # It can't be null, but otherwise you can't create new one
    product_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="product_owner", null=True)
    # It can't be null, but otherwise you can't create new one
    scrum_master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scrum_master", null=True)
    developers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="developers")

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
            scrum_master=self.scrum_master.api_data(self.id),
            product_owner=self.product_owner.api_data(self.id),
            developers=[user.api_data(self.id) for user in self.developers.all()],
            created_by=self.created_by.username,
            created=self.created,
            updated=self.updated,
        )
